import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from rich import print
from rich.prompt import Prompt
from rich.panel import Panel
import subprocess

# Load .env from current or parent directories
env_path = Path(".env")
if not env_path.exists():
    for parent in Path.cwd().parents:
        if (parent / ".env").exists():
            env_path = parent / ".env"
            break

load_dotenv(dotenv_path=env_path)

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=api_key)


### ---- TOOL FUNCTIONS ----

def run_command(cmd: str):
    """Run a shell command and return output/error with timeout and error handling."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)
        output = result.stdout + result.stderr
        print(f"[dim]{output.strip()}[/dim]")
        return output
    except subprocess.TimeoutExpired:
        return "[ERROR] Command timed out."
    except Exception as e:
        return f"[ERROR] {str(e)}"

def list_files(dir="."):
    files = []
    for root, dirs, filenames in os.walk(dir):
        for f in filenames:
            if f.startswith('.'):
                continue
            files.append(os.path.relpath(os.path.join(root, f), dir))
    return files

def read_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading {filepath}: {e}"

def write_file(filepath, content):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Wrote {filepath}"
    except Exception as e:
        return f"Error writing {filepath}: {e}"

def append_file(filepath, content):
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Appended to {filepath}"
    except Exception as e:
        return f"Error appending to {filepath}: {e}"

def create_file(filepath, content=""):
    return write_file(filepath, content)

def create_folder(folder):
    try:
        os.makedirs(folder, exist_ok=True)
        return f"Created folder {folder}"
    except Exception as e:
        return f"Error creating folder {folder}: {e}"

available_tools = {
    "run_command": run_command,
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "append_file": append_file,
    "create_file": create_file,
    "create_folder": create_folder,
}

SYSTEM_PROMPT = """
You are a terminal-based AI coding agent.
You help users build and modify full-stack projects.

Workflow:
- You follow a clear step-by-step loop: plan → action → observe → output.
- Only one plan step per prompt. Then proceed to action.
- You do not plan repeatedly. Plan once, then take an action.
- After action, wait for observation. Then decide next step.
- Use available tools to act on code.

Available Tools:
- "run_command": Run a terminal command.
- "list_files": List project files.
- "read_file": Read contents of a file.
- "write_file": Write (overwrite) contents of a file.
- "append_file": Append content to a file.
- "create_file": Create a new file with optional content.
- "create_folder": Create a new directory.

JSON Output Format:
{
  "step": "plan|action|observe|output",
  "content": "Your reasoning or message",
  "function": "If step is action, the function name",
  "input": "If step is action, the input to the function"
}

Example Interactions:

1. [PROJECT INITIALIZATION]
User: Create a React + Flask full-stack app.

AI:
{
  "step": "plan",
  "content": "I will create folder structure for a React frontend and a Flask backend."
}
{
  "step": "action",
  "function": "create_folder",
  "input": "frontend"
}
{
  "step": "action",
  "function": "create_folder",
  "input": "backend"
}
{
  "step": "action",
  "function": "run_command",
  "input": "npx create-react-app frontend"
}
{
  "step": "action",
  "function": "run_command",
  "input": "pip install flask"
}

---

2. [FEATURE ADDITION]
User: Now add a login page.

AI:
{
  "step": "plan",
  "content": "I will read the React frontend files to identify where to add the login component."
}
{
  "step": "action",
  "function": "list_files",
  "input": "frontend/src"
}
{
  "step": "action",
  "function": "read_file",
  "input": "frontend/src/App.js"
}
{
  "step": "action",
  "function": "create_file",
  "input": "frontend/src/Login.js"
}
{
  "step": "action",
  "function": "write_file",
  "input": {
    "path": "frontend/src/Login.js",
    "content": "import React from 'react';\nfunction Login() {\n  return <div>Login Page</div>;\n}\nexport default Login;"
  }
}
{
  "step": "action",
  "function": "append_file",
  "input": {
    "path": "frontend/src/App.js",
    "content": "\nimport Login from './Login';"
  }
}

---

3. [INSTALLATION COMMAND]
User: Install Tailwind CSS in the React app.

AI:
{
  "step": "plan",
  "content": "To install Tailwind, I will run npm commands inside the frontend directory."
}
{
  "step": "action",
  "function": "run_command",
  "input": "cd frontend && npm install -D tailwindcss postcss autoprefixer"
}
{
  "step": "action",
  "function": "run_command",
  "input": "cd frontend && npx tailwindcss init -p"
}

---

4. [CONTEXTUAL FOLLOW-UP]
User: Add an API route in Flask for login.

AI:
{
  "step": "plan",
  "content": "I will add a login route in the Flask backend inside app.py."
}
{
  "step": "action",
  "function": "read_file",
  "input": "backend/app.py"
}
{
  "step": "action",
  "function": "append_file",
  "input": {
    "path": "backend/app.py",
    "content": "\n@app.route('/login', methods=['POST'])\ndef login():\n    return {'status': 'success'}"
  }
}
"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def handle_tool(function, input_value):
    """Handles tool function calls, including dict-based file operations."""
    if function in ["write_file", "append_file", "create_file"]:
        # Accept dict or string input
        if isinstance(input_value, dict):
            path = input_value.get("path") or input_value.get("filepath")
            content = input_value.get("content", "")
            return available_tools[function](path, content)
        else:
            return available_tools[function](input_value)
    else:
        return available_tools[function](input_value)

def get_user_goal():
    user = Prompt.ask("[bold blue]>[/bold blue] [white]Your goal[/white]")
    return user

def handle_openai_response(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[red]OpenAI Error: {e}[/red]")
        return None

def process_plan_step(obj, content):
    print(f"[yellow]🧠 PLAN:[/yellow] {obj.get('content', '')}")
    messages.append({"role": "assistant", "content": content})

def _resolve_tool_input(fname, finput):
    """Helper to resolve tool input and call the appropriate handler."""
    if isinstance(finput, dict):
        return handle_tool(fname, finput)
    try:
        finput_obj = json.loads(finput)
        if isinstance(finput_obj, dict):
            return handle_tool(fname, finput_obj)
        else:
            return handle_tool(fname, finput)
    except Exception:
        return handle_tool(fname, finput)

def process_action_step(obj):
    fname = obj.get("function")
    finput = obj.get("input", "")
    print(f"[cyan]⚙ ACTION:[/cyan] {fname}('{finput}')")
    if fname not in available_tools:
        print(f"[red]Unknown tool: {fname}[/red]")
        return False
    try:
        result = _resolve_tool_input(fname, finput)
        messages.append({"role": "user", "content": json.dumps({"step": "observe", "output": result})})
        print(f"[magenta]🔍 OBSERVE:[/magenta] {result[:400]}{'...' if len(str(result)) > 400 else ''}")
    except Exception as e:
        print(f"[red]Tool execution failed: {e}[/red]")
        return False
    return True

def process_output_step(obj, content):
    print(Panel(obj.get("content", ""), title="[green]✅ OUTPUT[/green]"))
    messages.append({"role": "assistant", "content": content})

def process_step(obj, content):
    step = obj.get("step")
    if step == "plan":
        process_plan_step(obj, content)
        return "continue"
    elif step == "action":
        if not process_action_step(obj):
            return "break"
        return "continue"
    elif step == "output":
        process_output_step(obj, content)
        return "break"
    else:
        print(f"[red]❌ Unknown step: {step}[/red]")
        return "break"

def run_agent_steps():
    step_count = 0
    MAX_STEPS = 50  # prevent infinite loops

    while step_count < MAX_STEPS:
        step_count += 1
        content = handle_openai_response(messages)
        if content is None:
            break

        print("[grey]AI JSON Response:[/grey]")
        print(content)

        try:
            obj = json.loads(content)
        except Exception as e:
            print(f"[red]Invalid JSON: {e}[/red]")
            break

        result = process_step(obj, content)
        if result == "break":
            break
    else:
        print("[bold red]Maximum step count reached. Ending this task.[/bold red]")

def agent_chat_loop():
    print(Panel("💻 [bold green]Terminal Coding Agent Started[/bold green]\nType your goal, like 'Make a Flask app'", title="🧠 AI Agent", border_style="green"))

    while True:
        user = get_user_goal()
        if user.lower() in ["exit", "quit"]:
            print("[bold red]Goodbye![/bold red]")
            break

        messages.append({"role": "user", "content": user})
        run_agent_steps()

if __name__ == "__main__":
    try:
        agent_chat_loop()
    except KeyboardInterrupt:
        print("\n[bold red]Interrupted. Bye for now![/bold red]")