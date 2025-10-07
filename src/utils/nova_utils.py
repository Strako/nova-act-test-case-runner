from nova_act import ActAgentError, NovaAct
from classes.classes import StepResultArray, TestResult, Prompt
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


def execute_step(nova: NovaAct, step: str) -> StepResultArray:
    """
    Execute a single step in NovaAct and validate the response.
    """
    try:
        step = nova.act(step, schema=TestResult.model_json_schema())
        print(f"-----------------\n{step}")
        sesion_id = step.metadata.session_id
        act_id = step.metadata.act_id
        num_steps_executed = step.metadata.num_steps_executed
        prompt_text = step.metadata.prompt
    except ActAgentError as e:
        print(f"{STEP_ERROR} '{step}': {e}")
        return StepResultArray(
            parsed_step=TestResult(test_passed=False, error=e.message),
            sesion_id= e.metadata.session_id,
            act_id=e.metadata.act_id,
            num_steps_executed=e.metadata.num_steps_executed,
            prompt=step,
        )
    
    if not step.parsed_response:
        print(f"{NO_STEP_RESPONSE} '{step}'")
        return StepResultArray(
            parsed_step=TestResult(test_passed=True),
            sesion_id=sesion_id,
            act_id=act_id,
            num_steps_executed=num_steps_executed,
            prompt=prompt_text)
    
    try:
        parsed_step = TestResult.model_validate(step.parsed_response)
    except Exception as e:
        print(f"{ASSERT_STEP_ERROR} '{step}': {e}")
        parsed_step = TestResult(test_passed=False, error=f"{ASSERT_ERROR} {e}")


    return StepResultArray(
            parsed_step=parsed_step,
            sesion_id=sesion_id,
            act_id=act_id,
            num_steps_executed=num_steps_executed,
            prompt=prompt_text)


def run_test_case(nova: NovaAct, prompts: list[Prompt], input_list: list[str]) -> str:
    """
    Run a series of prompts in NovaAct and return an assertion.
    """

    for prompt in prompts:
        
        if prompt["type"] == "mail":
            act_result = execute_step(nova, prompt["step"])
            execute_input_step(nova, input_list[0])
            if not act_result.parsed_step.test_passed:
                print(f"{STEP_FAILED} {act_result.parsed_step.error}")
                return act_result

        if prompt["type"] == "password":
            act_result = execute_step(nova, prompt["step"])
            execute_input_step(nova, input_list[1])
            if not act_result.parsed_step.test_passed:
                print(f"{STEP_FAILED} {act_result.parsed_step.error}")
                return act_result

        if prompt['type'] == "none":
            act_result = execute_step(nova, prompt["step"])
            if not act_result.parsed_step.test_passed:
                print(f"{STEP_FAILED} {act_result.parsed_step.error}")
                return act_result     
       
    print(SUCCESS_TEST_CASE)
    return act_result


def simple_browse(starting_page: str, temp_folder: str) -> None:
    """
    Prompt user to browse manually int he provided host.
    """
    with NovaAct(starting_page=starting_page, user_data_dir=temp_folder, clone_user_data_dir=False):
        input(SIMPLE_BROWSE_MESSAGE)
