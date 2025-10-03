import os
import sys
import json
from dotenv import load_dotenv
from constants.constants import PROMPTS_FILE_ERROR, EMPTY_PROMPTS_ARRAY, UNKNOWN_ARGUMENT
from utils.export_results import export_results_to_excel
from utils.nova_utils import get_secret, run_test_case, simple_browse
from nova_act import NovaAct


load_dotenv()
logs_directory = os.getenv("LOGS_DIRECTORY")
temp_folder = os.getenv("TEMP_FOLDER")
secret_name = os.getenv("SECRET_NAME")

try:
    with open("prompts.json", "r", encoding="utf-8") as f:
        prompts_data = json.load(f)
    test_platform = prompts_data["test_platform"]
    test_cases = prompts_data["test_cases"]
except FileNotFoundError as e:
    print(f"{PROMPTS_FILE_ERROR}'{e}'")
    exit()

secret_object = json.loads(get_secret(secret_name))[test_platform]
user_mail = secret_object["mail"]
user_password = secret_object["password"]

input_list = [user_mail,user_password]

results_array = []

os.makedirs(temp_folder, exist_ok=True)
os.makedirs(logs_directory, exist_ok=True)




def run_workflow(record: bool):
    """Run the workflow from each test case provided by the JSON."""
    if not test_cases:
        print(EMPTY_PROMPTS_ARRAY)
        return []

    for test_case in test_cases:
        test_url = f"{test_case['route']}"

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
        "action": "login" | "record" | "default",
        "url": "<optional string, required for login>"
    }
    """
    action = event.get("action", "default").lower()

    if action == "login":
        url = event.get("url")
        if url and isinstance(url, str):
            simple_browse(url, temp_folder)
            return {"status": "login executed", "url": url}
        else:
            return {"error": "login requires a string 'url' in event"}

    elif action == "record":
        results = run_workflow(record=True)
        return {"status": "record executed", "results": results}

    elif action == "default":
        results = run_workflow(record=False)
        return {"status": "workflow executed", "results": results}

    else:
        return {"error": f"{UNKNOWN_ARGUMENT} {action}"}
