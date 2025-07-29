import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import httpx

from .models import Workflow, SystemInfo, CodeResult
from . import co_datascientist_api
from .kpi_extractor import extract_kpi_from_stdout, create_kpi_folder_name, should_enable_kpi_naming

OUTPUT_FOLDER = "co_datascientist_output"


def print_workflow_info(message: str):
    """Print workflow info with consistent formatting"""
    print(f"   {message}")


def print_workflow_step(message: str):
    """Print workflow step with consistent formatting"""
    print(f"   🔄 {message}")


def print_workflow_success(message: str):
    """Print workflow success with consistent formatting"""
    print(f"   ✅ {message}")


def print_workflow_error(message: str):
    """Print workflow error with consistent formatting"""
    print(f"   ❌ {message}")


class _WorkflowRunner:
    def __init__(self):
        self.workflow: Workflow | None = None
        self.start_timestamp = 0
        self.should_stop_workflow = False

    async def run_workflow(self, code: str, python_path: str, project_absolute_path: str, spinner=None):
        try:
            if spinner:
                spinner.text = "Initializing workflow..."
            self.start_timestamp = time.time()
            self.should_stop_workflow = False
            self.workflow = Workflow(status_text="Workflow started", user_id="")

            system_info = get_system_info(python_path)
            logging.info(f"user system info: {system_info}")
            
            if spinner:
                spinner.text = "Starting workflow..."
            response = await co_datascientist_api.start_workflow(code, system_info)
            self.workflow = response.workflow
            if spinner:
                spinner.stop()  # stop spinner without emoji
            print("Workflow started successfully")
            print()


            while not self.workflow.finished and response.code_to_run is not None and not self.should_stop_workflow:
                # Status information removed for minimal output
                # Stop spinner during code execution for clean output
                if spinner:
                    spinner.stop()
                
                print()  # Clean break instead of evaluating message
                
                result = _run_python_code(response.code_to_run.code, python_path)

                # Check if code execution failed and provide clear feedback
                if result.return_code != 0:
                    # Code failed - show error details
                    print_workflow_error(f"'{response.code_to_run.name}' failed with exit code {result.return_code}")
                    if result.stderr:
                        print("   📄 Error details:")
                        # Print each line of stderr with proper indentation
                        for line in result.stderr.strip().split('\n'):
                            print(f"      {line}")
                    
                    # For baseline failures, give specific guidance
                    if response.code_to_run.name == "baseline":
                        print("   💡 The baseline code failed to run. This will stop the workflow.")
                        print("   💡 Check the error above and fix your script before running again.")
                        if "ModuleNotFoundError" in (result.stderr or ""):
                            print("   💡 Missing dependencies? Try: pip install <missing-package>")
                else:
                    # Code succeeded - show success message
                    kpi_value = extract_kpi_from_stdout(result.stdout)
                    if kpi_value is not None:
                        print_workflow_success(f"Completed '{response.code_to_run.name}' | KPI = {kpi_value}")
                    else:
                        print_workflow_success(f"Completed '{response.code_to_run.name}'")

                # Extra space before the next spinner line
                print()

                # Restart spinner while waiting for next idea
                if spinner:
                    spinner.text = "Generating new idea..."
                    spinner.start()

                response = await co_datascientist_api.finished_running_code(self.workflow.workflow_id,
                                                                            response.code_to_run.code_version_id,
                                                                            result)
                self.workflow = response.workflow
                _update_output_folder(response.workflow, project_absolute_path)
                print()

            if self.should_stop_workflow:
                await co_datascientist_api.stop_workflow(self.workflow.workflow_id)
                print_workflow_info("Workflow stopped by user.")
                if spinner:
                    spinner.text = "Workflow stopped"
            else:
                # Check if workflow finished due to baseline failure or successful completion
                if (hasattr(self.workflow, 'baseline_code') and 
                    self.workflow.baseline_code.result is not None and 
                    self.workflow.baseline_code.result.return_code != 0):
                    print_workflow_error("Workflow terminated due to baseline code failure!")
                    print("   📄 Review the error details above and fix your script.")
                    if spinner:
                        spinner.text = "Workflow failed"
                else:
                    print_workflow_success("Workflow completed successfully!")
                    if spinner:
                        spinner.text = "Workflow completed"
                
        except httpx.HTTPStatusError as e:
            if spinner:
                spinner.text = "Error occurred"
            if e.response.status_code == 402:  # Payment Required - Usage limit exceeded
                try:
                    error_detail = e.response.json()
                    if error_detail.get('detail', {}).get('error') == 'usage_limit_exceeded':
                        print("\n🚨 FREE TOKENS EXHAUSTED!")
                        print(f"   {error_detail['detail']['message']}")
                        print(f"   Current usage: ${error_detail['detail']['current_usage_usd']}")
                        print(f"   Limit: ${error_detail['detail']['limit_usd']}")
                        print("\n💡 Check your usage status with: co-datascientist status")
                        print("💡 View detailed costs with: co-datascientist costs")
                        return
                except Exception:
                    pass
                print("\n🚨 Usage limit exceeded. Your free tokens have been exhausted.")
                print("   Use 'co-datascientist status' to check your usage.")
            elif e.response.status_code == 500:  # Internal Server Error - might be validation error
                try:
                    error_detail = e.response.json()
                    error_msg = error_detail.get('detail', str(e))
                    
                    # Check if it's an OpenAI key validation error
                    if "USER OPENAI KEY VALIDATION FAILED" in error_msg:
                        print(f"\n❌ {error_msg}")
                        return
                    else:
                        print(f"\n🚨 Server Error: {error_msg}")
                except Exception:
                    print(f"\n🚨 Server Error: {e}")
            else:
                print(f"\n❌ HTTP Error {e.response.status_code}: {e}")
            if self.workflow is not None:
                self.workflow.finished = True
                self.workflow.status_text = f"Workflow stopped due to error"
        except Exception as e:
            if spinner:
                spinner.text = "Error occurred"
            if self.workflow is not None:
                self.workflow.finished = True
                self.workflow.status_text = f"An error occurred while running workflow: {str(e)}"
            logging.exception("An error occurred while running workflow")
            print(f"\n❌ Error: {str(e)}")
            # Check if it might be a usage limit error
            if "402" in str(e) or "usage_limit_exceeded" in str(e):
                print("💡 This might be a usage limit error. Check with: co-datascientist status")


def _make_filesystem_safe(name):
    return re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", '_', name)


def _create_output_folder(project_absolute_path: str) -> None:
    output_path = Path(project_absolute_path) / OUTPUT_FOLDER
    output_path.mkdir(parents=True, exist_ok=True)


def _update_output_folder(workflow: Workflow, project_absolute_path: str) -> None:
    for code_version in workflow.code_versions:
        # Extract KPI from result if available and KPI naming is enabled
        base_folder_name = code_version.idea
        if should_enable_kpi_naming() and code_version.result is not None:
            try:
                kpi_value = extract_kpi_from_stdout(code_version.result.stdout)
                folder_name = _make_filesystem_safe(create_kpi_folder_name(base_folder_name, kpi_value))
            except Exception:
                # If KPI extraction fails for any reason, default to original naming
                folder_name = _make_filesystem_safe(base_folder_name)
        else:
            folder_name = _make_filesystem_safe(base_folder_name)
        
        timestamp = code_version.timestamp.strftime("%Y_%m_%d__%H_%M_%S")
        python_file_name = _make_filesystem_safe(f"{timestamp}_{code_version.name}.py")
        info_file_name = _make_filesystem_safe(f"{timestamp}_{code_version.name}_info.json")
        result_file_name = _make_filesystem_safe(f"{timestamp}_{code_version.name}_result.json")
        folder_path = Path(project_absolute_path) / OUTPUT_FOLDER / folder_name
        python_file_path = folder_path / python_file_name
        info_file_path = folder_path / info_file_name
        result_file_path = folder_path / result_file_name

        folder_path.mkdir(parents=True, exist_ok=True)
        if not python_file_path.exists():
            python_file_path.write_text(code_version.code)
        if not info_file_path.exists():
            info_file_path.write_text(json.dumps(code_version.info, indent=4) + "\n")
        if not result_file_path.exists():
            if code_version.result is not None:
                result_file_path.write_text(json.dumps(code_version.result.model_dump(), indent=4) + "\n")
            else:
                result_file_path.write_text("Result missing")


def _run_python_code(code: str, python_path: str) -> CodeResult:
    start_time = time.time()
    # write the code to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code.encode('utf-8'))
        temp_file_path = temp_file.name

    command = [python_path, temp_file_path]

    # run the command
    logging.info("running command: " + str(command))
    output = subprocess.run(command,
                            capture_output=True,
                            text=True,
                            input="",  # prevents it from blocking on stdin
                            timeout=300)  # TODO: change the timeout!
    return_code = output.returncode
    out = output.stdout
    err = output.stderr
    if isinstance(out, str) and out.strip() == "":
        out = None
    if isinstance(err, str) and err.strip() == "":
        err = None

    logging.info("stdout: " + str(out))
    logging.info("stderr: " + str(err))

    # delete the temporary file
    os.remove(temp_file_path)
    runtime_ms = int((time.time() - start_time) * 1000)
    return CodeResult(stdout=out, stderr=err, return_code=return_code, runtime_ms=runtime_ms)


def get_system_info(python_path: str) -> SystemInfo:
    return SystemInfo(
        python_libraries=_get_python_libraries(python_path),
        python_version=_get_python_version(python_path),
        os=sys.platform
    )


def _get_python_libraries(python_path: str) -> list[str]:
    try:
        # Use importlib.metadata to get installed packages (works in all Python 3.8+ environments)
        python_code = """
import importlib.metadata
for dist in importlib.metadata.distributions():
    print(f"{dist.metadata['Name']}=={dist.version}")
"""
        installed_libraries = subprocess.check_output(
            [python_path, "-c", python_code],
            universal_newlines=True
        ).strip()
        return [lib.strip() for lib in installed_libraries.split("\n") if lib.strip()]
    except subprocess.CalledProcessError:
        # If that fails, return empty list
        return []


def _get_python_version(python_path: str) -> str:
    return subprocess.check_output(
        [python_path, "--version"],
        universal_newlines=True
    ).strip()


workflow_runner = _WorkflowRunner()
