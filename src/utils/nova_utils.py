from nova_act import ActAgentError, NovaAct
from classes.classes import TestResult, Prompt
from constants.constants import *
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name:str):

    region_name = "us-east-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    
    return get_secret_value_response['SecretString']

def execute_input_step(nova: NovaAct, input:str):
            nova.page.keyboard.press(SELECT_ALL) 
            nova.page.keyboard.press(DELETE_KEY)
            nova.page.keyboard.type(input)


def execute_step(nova: NovaAct, prompt: str) -> TestResult:
    """
    Execute a single step in NovaAct and validate the response.
    """
    try:
        step = nova.act(prompt, schema=TestResult.model_json_schema())
    except ActAgentError as e:
        print(f"{STEP_ERROR} '{prompt}': {e}")
        return TestResult(test_passed=False, error=str(e))

    if not step.parsed_response:
        print(f"{NO_STEP_RESPONSE} '{prompt}'")
        return TestResult(test_passed=False, error=NO_AGENT_RESPONSE)

    try:
        parsed_step = TestResult.model_validate(step.parsed_response)
    except Exception as e:
        print(f"{ASSERT_STEP_ERROR} '{prompt}': {e}")
        return TestResult(test_passed=False, error=f"{ASSERT_ERROR} {e}")

    return parsed_step


def run_test_case(nova: NovaAct, prompts: list[Prompt], input_list: list[str]) -> str:
    """
    Run a series of prompts in NovaAct and return an assertion.
    """
    input_idx = 0

    for prompt in prompts:
        
        if prompt["type"] == "input":
            result = execute_step(nova, prompt["step"])
            execute_input_step(nova, input_list[input_idx])
            input_idx += 1
            if not result.test_passed:
                return f"{STEP_FAILED} {result.error}"
            
        result = execute_step(nova, prompt["step"])
        if not result.test_passed:
            return f"{STEP_FAILED} {result.error}"

    return SUCCESS_TEST_CASE


def simple_browse(starting_page: str, temp_folder: str) -> None:
    """
    Prompt user to browse manually int he provided host.
    """
    with NovaAct(starting_page=starting_page, user_data_dir=temp_folder, clone_user_data_dir=False):
        input(SIMPLE_BROWSE_MESSAGE)
