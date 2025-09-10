import os
import sys
import json
from dotenv import load_dotenv
from utils.nova_utils import run_test_case, simple_browse
from nova_act import NovaAct

load_dotenv()

base_url = os.getenv("HOST_URL")
temp_folder = "./temp-session"
os.makedirs(temp_folder, exist_ok=True)

with open("prompts.json", "r", encoding="utf-8") as f:
    prompts_data = json.load(f)
test_cases = prompts_data["test_cases"]
print(test_cases)

def main(record: bool):
    """Run the workflow from each test case provided by the JSON."""
    if not test_cases:
        print("No prompts to execute.")
        return
    for test_case in test_cases:
        with NovaAct(
            starting_page=f"{base_url}{test_case['route']}",
            user_data_dir=temp_folder,
            clone_user_data_dir=True,
            record_video=record
        ) as nova:
            result = run_test_case(nova, test_case["prompts"])
            print(result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if  sys.argv[1].lower() == "login":
            simple_browse(base_url, temp_folder)
        elif sys.argv[1].lower() == 'record':
            main(record=True)
        else:
            print(f"Unknown argument: {sys.argv[1]}")
    else:
        main(record=False)
