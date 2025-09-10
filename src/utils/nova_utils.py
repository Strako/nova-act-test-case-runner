from typing import Optional
from pydantic import BaseModel
from nova_act import ActAgentError, NovaAct

class TestResult(BaseModel):
    test_passed: bool
    error: Optional[str] = None

def execute_step(nova: NovaAct, prompt: str) -> TestResult:
    """
    Execute a single step in NovaAct and validate the response.
    """
    try:
        step = nova.act(prompt, schema=TestResult.model_json_schema())
    except ActAgentError as e:
        print(f"Error executing step '{prompt}': {e}")
        return TestResult(test_passed=False, error=str(e))

    if not step.parsed_response:
        print(f"No parsed_response returned for step '{prompt}'")
        return TestResult(test_passed=False, error="No response from agent")

    try:
        parsed_step = TestResult.model_validate(step.parsed_response)
    except Exception as e:
        print(f"Validation failed for step '{prompt}': {e}")
        return TestResult(test_passed=False, error=f"Validation failed: {e}")

    return parsed_step


def run_test_case(nova: NovaAct, prompts: list[str]) -> str:
    """
    Run a series of prompts in NovaAct and return an assertion.
    """
    for prompt in prompts:
        result = execute_step(nova, prompt)
        if not result.test_passed:
            return f"❌ Step failed: {result.error}"

    return "✅ All steps passed"


def simple_browse(starting_page: str, temp_folder: str) -> None:
    """
    Prompt user to browse manually int he provided host.
    """
    with NovaAct(starting_page=starting_page, user_data_dir=temp_folder, clone_user_data_dir=False):
        input("Log into your websites, then press enter...")
