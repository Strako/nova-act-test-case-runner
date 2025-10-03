# 🚧 NovaAct Web Testing Automation 🚧

```
🔨 UNDER CONSTRUCTION 🔨
⚠️  This project is currently in development phase  ⚠️
🚀 More features and improvements coming soon! 🚀
```

A Python-based web automation testing framework using NovaAct for browser automation and testing workflows. This framework enables automated testing of web applications with intelligent step execution, result validation, and comprehensive reporting.

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

- Python 3.8 or higher
- AWS Account (for Lambda deployment and Secrets Manager)
- NovaAct API Key
- Web browser (Chrome/Chromium recommended)

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd novaact-web-testing
   ```

2. **Install dependencies:**

   ```bash
   pip install -r src/requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the `src/` directory:

   ```env
   NOVA_ACT_API_KEY="your-nova-act-api-key"
   LOGS_DIRECTORY="./tmp/temp/"
   TEMP_FOLDER="./tmp/temp-session"
   SECRET_NAME="your-aws-secret-name"
   ```

4. **Configure AWS credentials** (for Secrets Manager access):
   ```bash
   aws configure
   ```

## ⚙️ Configuration

### Environment Variables

| Variable           | Description                     | Default              |
| ------------------ | ------------------------------- | -------------------- |
| `NOVA_ACT_API_KEY` | Your NovaAct API key            | Required             |
| `LOGS_DIRECTORY`   | Directory for storing logs      | `./tmp/temp/`        |
| `TEMP_FOLDER`      | Temporary session folder        | `./tmp/temp-session` |
| `SECRET_NAME`      | AWS Secrets Manager secret name | Required             |

### AWS Secrets Manager Setup

Store your test credentials in AWS Secrets Manager with the following structure:

```json
{
  "your-platform-name": {
    "mail": "test@example.com",
    "password": "your-password"
  }
}
```

## 🚀 Usage

### Local Execution

1. **Run tests without recording:**

   ```bash
   cd src
   python main.py
   ```

2. **Run tests with video recording:**

   ```bash
   cd src
   python main.py record
   ```

3. **Manual login/browsing:**
   ```bash
   cd src
   python main.py login https://your-test-site.com
   ```

### Command Line Options

- `python main.py` - Run all test cases without recording
- `python main.py record` - Run all test cases with video recording
- `python main.py login <URL>` - Open browser for manual login/browsing

## 📄 JSON Configuration

### Test Configuration Structure

Create your test configuration in `prompts.json`:

```json
{
  "test_platform": "your-platform-name",
  "test_cases": [
    {
      "id": 1,
      "route": "https://your-test-site.com",
      "description": "Test case description",
      "prompts": [
        {
          "step": "Click on email field",
          "type": "input"
        },
        {
          "step": "Click on password field",
          "type": "input"
        },
        {
          "step": "Click login button",
          "type": "none"
        },
        {
          "step": "Verify welcome message appears",
          "type": "none"
        }
      ]
    }
  ]
}
```

### Prompt Types

- **`input`**: Steps that require user input (email, password, etc.)
- **`none`**: Steps that don't require input (clicks, validations, etc.)

## 📊 Results Export and Chain of Thought Capture

The framework automatically captures and exports:

- **Session metadata** (session ID, act ID, step count)
- **Test execution results** (pass/fail status, errors)
- **Chain of thought data** from NovaAct's decision process
- **Excel reports** with comprehensive test results

### Export Features

- Automatic Excel file generation (`results.xlsx`)
- Detailed step-by-step execution logs
- Error tracking and reporting
- Session replay capabilities

## 📈 Understanding the Results

### Result Structure

Each test execution generates:

```python
{
    "session_id": "unique-session-identifier",
    "act_id": "action-identifier",
    "test_case_id": 1,
    "num_steps_executed": 4,
    "description": "Test case description",
    "prompt": "Last executed prompt",
    "test_passed": True/False,
    "error": "Error message if failed"
}
```

### Status Indicators

- ✅ **Success**: All steps passed
- ❌ **Failed**: Step validation failed
- ⚠️ **Error**: Execution error occurred

## ☁️ Deployment to AWS Lambda

### Build Deployment Package

```bash
cd src
make build
```

This creates `my_deployment_package.zip` ready for Lambda deployment.

### Lambda Configuration

- **Runtime**: Python 3.8+
- **Handler**: `lambda_function.lambda_handler`
- **Timeout**: 15 minutes (recommended)
- **Memory**: 1024 MB (minimum)

### Lambda Event Structure

```json
{
  "action": "default|record|login",
  "url": "https://example.com" // Required for login action
}
```

### Lambda Response

```json
{
  "status": "workflow executed",
  "results": [
    /* test results array */
  ]
}
```

## 📁 Project Structure

```
src/
├── classes/
│   ├── __init__.py
│   └── classes.py          # Pydantic models and type definitions
├── constants/
│   ├── __init__.py
│   └── constants.py        # Application constants and messages
├── libraries/              # Packaged dependencies for Lambda
├── tmp/                    # Temporary files and logs
├── utils/
│   ├── __init__.py
│   ├── export_results.py   # Excel export functionality
│   ├── export_utils.py     # Export utility functions
│   └── nova_utils.py       # NovaAct integration utilities
├── .env                    # Environment configuration
├── lambda_function.py      # AWS Lambda entry point
├── main.py                 # Local execution entry point
├── makefile               # Build automation
├── prompts.json           # Test configuration
└── requirements.txt       # Python dependencies
```

## 🛠️ Utilities

### Core Utilities

- **`nova_utils.py`**: NovaAct integration, step execution, AWS Secrets Manager
- **`export_results.py`**: Excel report generation
- **`export_utils.py`**: Data processing and formatting utilities

### Key Functions

- `run_test_case()`: Execute a complete test case
- `execute_step()`: Execute individual test steps
- `get_secret()`: Retrieve credentials from AWS Secrets Manager
- `export_results_to_excel()`: Generate Excel reports

## 📦 Dependencies

### Core Dependencies

```
python-dotenv    # Environment variable management
pydantic        # Data validation and serialization
nova-act        # Web automation framework
boto3           # AWS SDK
openpyxl        # Excel file generation
```

### Development Dependencies

All dependencies are automatically managed through `requirements.txt`.

## 🔍 Troubleshooting

### Common Issues

1. **NovaAct API Key Issues**

   ```
   Error: Invalid API key
   Solution: Verify NOVA_ACT_API_KEY in .env file
   ```

2. **AWS Secrets Manager Access**

   ```
   Error: Unable to retrieve secret
   Solution: Check AWS credentials and secret name
   ```

3. **Browser Automation Issues**

   ```
   Error: Browser launch failed
   Solution: Ensure Chrome/Chromium is installed
   ```

4. **File Not Found: prompts.json**
   ```
   Error: prompts.json not found
   Solution: Copy prompts_example.json to prompts.json and configure
   ```

### Debug Mode

Enable verbose logging by setting environment variables:

```bash
export NOVA_ACT_DEBUG=true
export LOGS_DIRECTORY="./debug-logs/"
```

### Log Files

- Session logs: `./tmp/temp/`
- Video recordings: Available when using `record` mode
- Excel reports: `results.xlsx` in project root

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include docstrings for public methods
- Write tests for new functionality
- Update documentation as needed

### Code Style

```python
def example_function(param: str) -> bool:
    """
    Example function with proper typing and documentation.

    Args:
        param: Description of parameter

    Returns:
        Boolean indicating success
    """
    return True
```

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the troubleshooting section
- Review the NovaAct documentation

---

_This project uses NovaAct for web automation. Make sure you have proper API credentials configured._

**Note**: This project is under active development. Features and APIs may change between versions.
