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
- [Project Structure](#project-structure)
- [JSON Configuration](#json-configuration)
- [Utilities](#utilities)
- [Arguments](#arguments)

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
```

#### Environment Variables Explanation

| Variable           | Description                                               | Example                                |
| ------------------ | --------------------------------------------------------- | -------------------------------------- |
| `NOVA_ACT_API_KEY` | Your NovaAct API key for browser automation               | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `HOST_URL`         | Base URL of the target website **without trailing slash** | `https://example.com`                  |

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

## 📁 Project Structure

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
│   └── nova_utils.py      # NovaAct utility functions and AWS integration
└── temp-session/          # Browser session data (auto-created)
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

## 🐛 Troubleshooting

### Common Issues

1. **"prompts.json not found"**: Make sure to rename `propmts_example.json` to `prompts.json`
2. **Import errors**: Ensure virtual environment is activated and dependencies are installed
3. **NovaAct API errors**: Verify your API key in the `.env` file
4. **AWS Secrets Manager errors**: Check your AWS credentials and region configuration
5. **Missing import error for `get_secret`**: Add the import in `main.py`: `from utils.nova_utils import get_secret`
6. **Keyboard shortcut issues**: The app uses macOS shortcuts (`Meta+A`, `Backspace`) - may need adjustment for other OS
7. **JSON structure errors**: Ensure prompts follow the new object format with `step` and `type` fields

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
