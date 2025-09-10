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
├── constants/
│   ├── __init__.py
│   └── constants.py       # Application constants and messages
├── utils/
│   ├── __init__.py
│   └── nova_utils.py      # NovaAct utility functions
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
        "Given: El usuario hace click en el botón Jugar, en caso de error retorna un error",
        "When: El usuario accede al juego correctamente y se carga la interfaz del memorama"
      ]
    }
  ]
}
```

### JSON Structure Explanation

- **`test_cases`**: Array of test case objects
- **`route`**: URL path to append to the base HOST_URL
- **`prompts`**: Array of natural language instructions for the automation agent

## 🛠️ Utilities

### `nova_utils.py` Functions

#### `execute_step(nova: NovaAct, prompt: str) -> TestResult`

- Executes a single automation step using NovaAct
- Validates the response using Pydantic models
- Returns a `TestResult` object with success status and error details

#### `run_test_case(nova: NovaAct, prompts: list[str]) -> str`

- Runs a complete test case with multiple prompts
- Stops execution on first failure
- Returns success message or error details

#### `simple_browse(starting_page: str, temp_folder: str) -> None`

- Opens a browser session for manual interaction
- Useful for login processes or manual testing
- Waits for user input before closing

### `constants.py`

Contains all application constants including:

- Error messages with colored formatting
- Success indicators with emojis
- User interaction prompts

## 🔍 Dependencies

- **`python-dotenv`**: Environment variable management
- **`pydantic`**: Data validation and parsing
- **`nova-act`**: Browser automation framework

## 🐛 Troubleshooting

### Common Issues

1. **"prompts.json not found"**: Make sure to rename `propmts_example.json` to `prompts.json`
2. **Import errors**: Ensure virtual environment is activated and dependencies are installed
3. **NovaAct API errors**: Verify your API key in the `.env` file

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
