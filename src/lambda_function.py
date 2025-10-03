import os
import json
from dotenv import load_dotenv
from constants.constants import PROMPTS_FILE_ERROR, EMPTY_PROMPTS_ARRAY, UNKNOWN_ARGUMENT
from utils.export_results import export_results_to_excel
from utils.nova_utils import get_secret, run_test_case, simple_browse
from nova_act import NovaAct

# Load env variables
load_dotenv()
base_url = os.getenv("HOST_URL")
logs_directory = os.getenv("LOGS_DIRECTORY")
temp_folder = os.getenv("TEMP_FOLDER")
secret_name = os.getenv("SECRET_NAME")
mach0_user = json.loads(get_secret(secret_name))["mach9_user"]
user_mail = mach0_user["mail"]
user_password = mach0_user["password"]

input_list = [user_mail, user_password]
results_array = []

os.makedirs(temp_folder, exist_ok=True)

try:
    with open("prompts.json", "r", encoding="utf-8") as f:
        prompts_data = json.load(f)
    test_cases = prompts_data["test_cases"]
except FileNotFoundError as e:
    print(f"{PROMPTS_FILE_ERROR}'{e}'")
    test_cases = []


def run_workflow(record: bool):
    """Run the workflow for each test case provided by the JSON."""
    if not test_cases:
        print(EMPTY_PROMPTS_ARRAY)
        return []

    for test_case in test_cases:
        test_url = f"{base_url}{test_case['route']}"

        with NovaAct(
            starting_page=test_url,
            logs_directory=logs_directory,
            user_data_dir=temp_folder,
            clone_user_data_dir=True,
            record_video=record
        ) as nova:
            result = run_test_case(nova, test_case["prompts"], input_list)
            print(result)
            row = {
                "session_id": result.sesion_id,
                "act_id": result.act_id,
                "test_case_id": test_case["id"],
                "num_steps_executed": result.num_steps_executed,
                "description": test_case["description"],
                "prompt": result.prompt,
                "test_passed": result.parsed_step.test_passed,
                "error": result.parsed_step.error
            }
            results_array.append(row)

    export_results_to_excel(results_array)
    return results_array


def lambda_handler(event, context):
    """
    AWS Lambda entry point.
    event should contain:
    {
        "action": "login" | "record" | "default"
    }
    """
    action = event.get("action", "default").lower()

    if action == "login":
        simple_browse(base_url, temp_folder)
        return {"status": "login executed"}
    elif action == "record":
        results = run_workflow(record=True)
        return {"status": "record executed", "results": results}
    elif action == "default":
        results = run_workflow(record=False)
        return {"status": "workflow executed", "results": results}
    else:
        return {"error": f"{UNKNOWN_ARGUMENT} {action}"}
