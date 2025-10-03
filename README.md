# 🚧 NovaAct Web Testing Automation 🚧

```
🔨 UNDER CONSTRUCTION 🔨
⚠️  This project is currently in development phase  ⚠️
🚀 More features and improvements coming soon! 🚀
```

A Python-based web automation testing framework using NovaAct for browser automation and testing workflows.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [JSON Configuration](#json-configuration)
- [Results Export and Chain of Thought Capture](#results-export-and-chain-of-thought-capture)
- [Understanding the Results](#understanding-the-results)
- [Deployment to AWS Lambda](#deployment-to-aws-lambda)
- [Project Structure](#project-structure)
- [Utilities](#utilities)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🔧 Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create and Activate Virtual Environment

#### Windows

```cmd
# Create virtual environment
python -m venv env

# Activate virtual environment
env\Scripts\activate
```

#### Linux/macOS

```bash
# Create virtual environment
python3 -m venv env

# Activate virtual environment
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r src/requirements.txt
```

## ⚙️ Configuration

### 1. Environment Variables

Create or configure your `.env` file in the `src/` directory with the following structure:

**File: `src/.env`**

```env
NOVA_ACT_API_KEY=your-nova-act-api-key-here
HOST_URL=https://your-target-website.com
LOGS_DIRECTORY=./temp/
SECRET_NAME=mach9_user
```

#### Environment Variables Explanation

| Variable           | Description                                                                   | Example                                |
| ------------------ | ----------------------------------------------------------------------------- | -------------------------------------- |
| `NOVA_ACT_API_KEY` | Your NovaAct API key for browser automation                                   | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `HOST_URL`         | Base URL of the target website **without trailing slash**                     | `https://example.com`                  |
| `LOGS_DIRECTORY`   | **🆕 Directory where NovaAct saves execution logs and chain of thought data** | `./temp/`                              |
| `SECRET_NAME`      | **🆕 Name of the AWS Secrets Manager secret containing user credentials**     | `mach9_user`                           |

**Important Notes:**

- The `HOST_URL` should NOT end with a forward slash (`/`)
- Routes from `prompts.json` will be appended to this base URL
- Example: `HOST_URL` + `route` = `https://example.com` + `/welcome` = `https://example.com/welcome`

### 2. Test Configuration

**Important**: Rename the example prompts file to start using the application:

```bash
mv src/propmts_example.json src/prompts.json
```

## 🚀 Usage

### Prerequisites for AWS Integration

The application now integrates with AWS Secrets Manager for secure credential management. Ensure you have:

1. **AWS Credentials configured** (via AWS CLI, environment variables, or IAM roles)
2. **Access to AWS Secrets Manager** in the `us-east-2` region
3. **A secret named `mach9_user`** containing user credentials in JSON format:
   ```json
   {
     "mach9_user": {
       "mail": "user@example.com",
       "password": "userpassword"
     }
   }
   ```

### Running the Application

Navigate to the `src` directory and run the main script:

```bash
cd src
python3.11 main.py [ARGUMENT]
```

### Available Arguments

| Argument        | Description                                       |
| --------------- | ------------------------------------------------- |
| `login`         | Opens a browser session for manual login/browsing |
| `record`        | Runs test cases with video recording enabled      |
| _(no argument)_ | Runs test cases without video recording           |

### Examples

```bash
# Run tests without recording
python3.11 main.py

# Run tests with video recording
python3.11 main.py record

# Open browser for manual login
python3.11 main.py login
```

## 📝 JSON Configuration

The `prompts.json` file defines your test cases with the following structure:

```json
{
  "test_cases": [
    {
      "route": "/welcome",
      "prompts": [
        {
          "step": "Click on the login button",
          "type": "none"
        },
        {
          "step": "Fill in the email field",
          "type": "input"
        },
        {
          "step": "Fill in the password field",
          "type": "input"
        },
        {
          "step": "Click submit and verify successful login",
          "type": "none"
        }
      ]
    }
  ]
}
```

### JSON Structure Explanation

- **`test_cases`**: Array of test case objects
- **`route`**: URL path to append to the base HOST_URL
- **`prompts`**: Array of prompt objects with step instructions and input types

### Prompt Object Structure

- **`step`**: Natural language instruction for the automation agent
- **`type`**: Defines the prompt behavior:
  - `"none"`: Standard automation step without input
  - `"input"`: Step that requires text input (uses AWS Secrets Manager credentials)

## 📊 Results Export and Chain of Thought Capture

### New Export Features

The application now automatically captures and exports the **chain of thought** (reasoning process) from NovaAct's decision-making process:

- **Automatic Chain of Thought Capture**: All `rawProgramBody` data from NovaAct's reasoning process is automatically collected
- **Enhanced Excel Export**: Results are exported to `results.xlsx` with a new `rawProgramBody` column containing the complete reasoning chain
- **Session-based Data Collection**: Uses `session_id` to locate and process all JSON files from each test execution
- **Concatenated Output**: Multiple reasoning steps are joined with newlines for readable Excel display

### Export Process Flow

1. **Test Execution**: NovaAct runs tests and saves detailed logs to `./temp/{session_id}/`
2. **Data Collection**: After test completion, the system scans all JSON files in the session folder
3. **Chain of Thought Extraction**: Extracts `response.rawProgramBody` from each JSON object
4. **Excel Export**: Adds all reasoning steps to the `rawProgramBody` column in `results.xlsx`

### Chain of Thought Data Structure

Each JSON file in `./temp/{session_id}/` contains an array of objects with this structure:

```json
[
  {
    "request": { ... },
    "response": {
      "rawProgramBody": "think(\"My reasoning process here...\");\nagentClick(\"selector\");"
    }
  }
]
```

The `rawProgramBody` field contains:

- **Reasoning statements**: `think("...")` showing the AI's decision-making process
- **Action commands**: `agentClick()`, `agentType()`, etc. showing what actions were taken
- **Complete execution flow**: Step-by-step breakdown of how each test was executed

### Example Chain of Thought Output

```
think("My task is to click on the 'Iniciar sesión' button. I am on a login page, so I assume the 'Iniciar sesión' button is the one that will submit the login form. I should click the 'Iniciar sesión' button to select it.");
agentClick(" <box>573,631,620,968</box> ");

think("I am now on a home page with the text '¡Bienvenido, armando isai!', so my last action was successful. I have completed the task, since I was not asked to perform any actions after clicking the 'Iniciar sesión' button.");
return;
```

### Results.xlsx Structure

The exported Excel file now contains these columns:

| Column               | Description                                            |
| -------------------- | ------------------------------------------------------ |
| `session_id`         | Unique identifier for the test session                 |
| `act_id`             | Individual action identifier                           |
| `test_case_id`       | Test case identifier from prompts.json                 |
| `num_steps_executed` | Number of steps completed                              |
| `description`        | Test case description                                  |
| `prompt`             | The prompt that was executed                           |
| `test_passed`        | Boolean indicating test success                        |
| `error`              | Error message if test failed                           |
| **`rawProgramBody`** | **🆕 Complete chain of thought and reasoning process** |

## 📈 Understanding the Results

### Analyzing Chain of Thought Data

The `rawProgramBody` column in `results.xlsx` provides valuable insights:

- **Decision Making**: See exactly how NovaAct reasoned through each step
- **Action Mapping**: Understand which UI elements were targeted and why
- **Error Analysis**: When tests fail, review the reasoning to identify issues
- **Test Optimization**: Use insights to improve prompt clarity and test reliability

### Data Locations

- **Test Results**: `results.xlsx` (generated after each run)
- **Raw Logs**: `./temp/{session_id}/` (detailed JSON files with complete execution data)
- **Session Data**: `./temp-session/` (browser session information)

## 🚀 Deployment to AWS Lambda

This project includes a makefile that automates the packaging process for AWS Lambda deployment. The makefile creates a deployment package that includes all necessary dependencies while excluding development files.

### Makefile

The makefile provides three main commands:

#### `make build` (or just `make`)

- **Installs dependencies**: Downloads all packages from `requirements.txt` into a `./libraries` directory
- **Creates base package**: Zips all dependencies from the libraries folder
- **Adds source code**: Includes all project files except excluded ones (main.py, makefile, and libraries folder)
- **Generates deployment package**: Creates `my_deployment_package.zip` ready for Lambda upload

#### `make clean`

- **Removes build artifacts**: Deletes the `./libraries` directory
- **Cleans deployment package**: Removes the generated `my_deployment_package.zip` file

#### Files Excluded from Lambda Package

The makefile automatically excludes these files from the deployment package:

- `main.py` (local development entry point)
- `makefile` (build script)
- `./libraries/*` (temporary dependency folder)

### Lambda Deployment Steps

1. **Navigate to the src directory**:

   ```bash
   cd src
   ```

2. **Build the deployment package**:

   ```bash
   make build
   ```

3. **Upload to AWS Lambda**:

   - Use the generated `my_deployment_package.zip` file
   - Set the Lambda handler to `lambda_function.lambda_handler`
   - Configure environment variables as needed

4. **Clean up build files** (optional):
   ```bash
   make clean
   ```

### Lambda Function Entry Point

The project includes `lambda_function.py` as the entry point for AWS Lambda execution, separate from the local development `main.py` file.

#### Event Structure

When invoking the Lambda function, the event should contain an `action` field that determines the execution mode:

```json
{
  "action": "login" | "record" | "default"
}
```

**Action Types:**

- `"login"` - Opens a browser session for manual login/browsing
- `"record"` - Runs test cases with video recording enabled
- `"default"` - Runs test cases without video recording (same as no argument in local execution)

**Example Lambda Event:**

```json
{
  "action": "record"
}
```

## � Project Structure

```
src/
├── .env                    # Environment variables
├── main.py                 # Main application entry point
├── prompts.json           # Test cases configuration (rename from propmts_example.json)
├── propmts_example.json   # Example test cases template
├── requirements.txt       # Python dependencies
├── classes/
│   ├── __init__.py
│   └── classes.py         # Pydantic models and TypedDict definitions
├── constants/
│   ├── __init__.py
│   └── constants.py       # Application constants and messages
├── utils/
│   ├── __init__.py
│   ├── nova_utils.py      # NovaAct utility functions and AWS integration
│   ├── export_utils.py    # 🆕 Chain of thought processing utilities
│   └── export_results.py  # 🆕 Enhanced Excel export with reasoning data
├── temp-session/          # Browser session data (auto-created)
├── temp/                  # 🆕 NovaAct execution logs and chain of thought data
│   └── {session_id}/      # 🆕 Session-specific folders containing JSON files
└── results.xlsx           # 🆕 Generated Excel file with test results and reasoning
```

## 🛠️ Utilities

### `nova_utils.py` Functions

#### `get_secret() -> str`

- Retrieves user credentials from AWS Secrets Manager
- Uses boto3 to connect to the region you have configured inside **`~/.aws/config`**
- Returns secret string containing user authentication data

#### `execute_input_step(nova: NovaAct, input: str) -> None`

- Handles text input automation for form fields
- Clears existing field content and types new input
- Uses keyboard shortcuts for selection and deletion

#### `execute_step(nova: NovaAct, prompt: str) -> TestResult`

- Executes a single automation step using NovaAct
- Validates the response using Pydantic models
- Returns a `TestResult` object with success status and error details

#### `run_test_case(nova: NovaAct, prompts: list[Prompt], input_list: list[str]) -> str`

- Runs a complete test case with multiple prompts
- Handles both standard steps and input steps
- Uses AWS credentials for input fields when `type: "input"`
- Stops execution on first failure
- Returns success message or error details

#### `simple_browse(starting_page: str, temp_folder: str) -> None`

- Opens a browser session for manual interaction
- Useful for login processes or manual testing
- Waits for user input before closing

### `export_utils.py` Functions 🆕

#### `process_results_with_raw_program_body(results_array) -> List[Dict]`

- **Main processing function** that enriches results with chain of thought data
- Uses `session_id` to locate corresponding JSON files in `./temp/{session_id}/`
- Extracts all `response.rawProgramBody` entries from JSON files
- Returns enhanced results array with `rawProgramBody` field

#### `_extract_raw_program_body_from_item(item) -> str | None`

- Extracts `rawProgramBody` from a single JSON object
- Validates structure: `item.response.rawProgramBody`
- Returns the reasoning string or None if not found

#### `_process_json_file(json_file) -> List[str]`

- Processes a single JSON file and extracts all `rawProgramBody` strings
- Handles JSON arrays and iterates through each object
- Returns list of reasoning strings from the file

#### `_get_raw_program_bodies_for_session(session_id) -> List[str]`

- Collects all `rawProgramBody` entries for a specific session
- Scans all JSON files in the session folder
- Returns combined list of reasoning strings

#### `_process_single_result(result) -> Dict`

- Processes one result object to add `rawProgramBody` data
- Uses session_id to find and process corresponding JSON files
- Returns enhanced result with reasoning data

#### `_format_cell_value(header, value) -> str`

- Formats values for Excel export
- Joins `rawProgramBody` arrays with newlines for readability
- Handles None values and type conversion

#### `_create_excel_row(result, headers) -> List[str]`

- Creates a formatted row for Excel export
- Uses `_format_cell_value()` for proper formatting
- Returns list of formatted cell values

### `export_results.py` Functions

#### `export_results_to_excel(results_array, output_file="results.xlsx")`

- **Enhanced main export function** with chain of thought integration
- Automatically processes results using `process_results_with_raw_program_body()`
- Creates Excel file with all columns including the new `rawProgramBody` column
- Uses helper functions from `export_utils.py` for consistent formatting

### `classes.py` Models

#### `TestResult(BaseModel)`

- Pydantic model for test execution results
- Fields: `test_passed: bool`, `error: Optional[str]`

#### `Prompt(TypedDict)`

- Type definition for prompt objects in JSON configuration
- Fields: `step: str`, `type: Literal["input", "none"]`

### `constants.py`

Contains all application constants including:

- Error messages with colored formatting
- Success indicators with emojis
- User interaction prompts

## 🔍 Dependencies

- **`python-dotenv`**: Environment variable management
- **`pydantic`**: Data validation and parsing
- **`nova-act`**: Browser automation framework
- **`boto3`**: AWS SDK for Python (Secrets Manager integration)
- **`openpyxl`**: Excel file creation and manipulation
- **`glob`**: File pattern matching for JSON processing
- **`json`**: JSON data parsing and processing

## 🐛 Troubleshooting

### Common Issues

1. **"prompts.json not found"**: Make sure to rename `propmts_example.json` to `prompts.json`
2. **Import errors**: Ensure virtual environment is activated and dependencies are installed
3. **NovaAct API errors**: Verify your API key in the `.env` file
4. **AWS Secrets Manager errors**: Check your AWS credentials and region configuration
5. **Missing import error for `get_secret`**: Add the import in `main.py`: `from utils.nova_utils import get_secret`
6. **Keyboard shortcut issues**: The app uses macOS shortcuts (`Meta+A`, `Backspace`) - may need adjustment for other OS
7. **JSON structure errors**: Ensure prompts follow the new object format with `step` and `type` fields
8. **🆕 Empty rawProgramBody column**: Check that `LOGS_DIRECTORY=./temp/` is set correctly in `.env`
9. **🆕 Missing chain of thought data**: Verify that JSON files exist in `./temp/{session_id}/` after test execution

### Error Messages

The application provides colored error messages to help identify issues:

- ❌ Red messages indicate critical errors
- ⚠️ Yellow warnings for configuration issues
- ✅ Green checkmarks for successful operations

## 🤝 Contributing

We welcome contributions to improve this project! Please follow these guidelines:

### How to Contribute

1. **Fork the Repository**

   - Click the "Fork" button on the top right of this repository
   - Clone your forked repository to your local machine

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**

   - Follow the existing code style and conventions
   - Add tests for new functionality when applicable
   - Update documentation as needed

4. **Test Your Changes**

   - Ensure all existing tests pass
   - Test your new features thoroughly
   - Verify the application runs correctly with your changes

5. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "Add: descriptive commit message"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your feature branch
   - Provide a clear description of your changes
   - Reference any related issues

### Contribution Guidelines

- **Code Quality**: Maintain clean, readable, and well-documented code
- **Testing**: Include tests for new features and bug fixes
- **Documentation**: Update README.md and inline comments as needed
- **Commit Messages**: Use clear, descriptive commit messages
- **Issue Reporting**: Use GitHub Issues to report bugs or suggest features

### Development Setup

Follow the installation instructions in this README to set up your development environment.

Thank you for contributing to make this project better! 🚀

---

_This project uses NovaAct for web automation. Make sure you have proper API credentials configured._
