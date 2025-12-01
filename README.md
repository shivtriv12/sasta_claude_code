# Sasta Claude Code

**Sasta Claude Code** is a CLI-based AI agent capable of exploring local codebases, diagnosing issues, and executing complex programming tasks.

## Installation & Setup

### Prerequisites

- Python 3.10+
- A Google Gemini API Key

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/shivtriv12/sasta_claude_code.git
   cd sasta_claude_code
   ```

2. **Install Dependencies**
   This project uses `uv`.

   ```bash
   uv add google-genai python-dotenv
   ```

3. **Environment Setup**
   Create a `.env` file in the root directory and add your API key:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

## How to Run

Run the main script to start the interactive session. By default, it operates in the `./calculator` directory (configurable).

```bash
uv run main.py "your prompt" --verbose #optional
```

## Project Structure

Here is a breakdown of the codebase to help you understand how the agent works:

### Core Logic

- **`main.py`**: The heart of the application. It initializes the Gemini client, manages the chat history, and handles the "Think -> Act -> Observe" loop.
- **`config.py`**: Central configuration file. Controls settings like `WORKING_DIRECTORY` (where the agent is allowed to touch files) and `MAX_CHARS` (context limits).
- **`prompts.py`**: Contains the **System Prompt**. This defines the agent's persona, rules, and instructions on how to use tools effectively.
- **`available_functions.py`**: Defines the **Tool Schemas** sent to the Gemini API. This tells the LLM _what_ tools are available (e.g., "I have a tool to read files").

### Tool Implementations (`functions/`)

The "hands" of the agent. These scripts perform the actual OS operations:

- **`functions/get_files_info.py`**: Returns a recursive tree view of the directory structure so the agent can "see" the project layout.
- **`functions/get_file_content.py`**: Reads the content of specific files.
- **`functions/write_file_content.py`**: Creates or overwrites files with new code.
- **`functions/run_python_file.py`**: Executes a Python script using `subprocess`. It captures `stdout` and `stderr` so the agent knows if its code worked or crashed.
- **`functions/call_function.py`**: A utility that maps the API's tool call requests to these local Python functions.

### Sample Project (`calculator/`)

A sandbox environment containing a simple calculator app. This is used to test the agent's ability to find bugs and write tests without risking your main system.
