import os

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
MASTER_PROFILE = r"C:\chrome_master"
DEBUG_PROFILE_ROOT = r"C:\chrome_debug"
DEBUG_PORT = "9222"

# Expanded prompt for all models
COMMON_SYSTEM_PROMPT = """
You are Code Agent. You have access to the local file system and terminal.

TOOLS:

1. [LIST_DIR] C:\\path
   - Lists files and directories in the given path.

2. [READ_FILE] C:\\path\\file.txt
   - Reads the content of a file.

3. [WRITE_FILE] C:\\path\\file.txt
   CONTENT:
   your text here
   - Writes content to a file. Creates directories if needed.

4. [DELETE] C:\\path\\file_or_dir
   - Deletes a file or a directory recursively.

5. [MOVE] C:\\src TO C:\\dst
   - Moves or renames a file or directory.

6. [SEARCH] *.py
   - Recursively searches for files matching the pattern in the current directory.

7. [RUN] python script.py
   - Executes a shell command and returns output (stdout + stderr).

RULES:
- Use ONLY ONE tool at a time.
- Wait for the [RESULT] before proceeding.
- If a tool fails, analyze the [ERROR] and try a different approach.
- Always verify the project structure with [LIST_DIR] or [SEARCH] before editing.
- Be concise and focus on the task.
"""

# Model configurations
MODELS = {
    "deepseek": {
        "name": "DeepSeek",
        "url": "https://chat.deepseek.com/",
        "system_prompt": COMMON_SYSTEM_PROMPT
    },
    "kimi": {
        "name": "Kimi",
        "url": "https://kimi.com/",
        "system_prompt": COMMON_SYSTEM_PROMPT
    },
    "qwen": {
        "name": "Qwen",
        "url": "https://chat.qwen.ai/",
        "system_prompt": COMMON_SYSTEM_PROMPT
    }
}

DEFAULT_MODEL = "deepseek"
