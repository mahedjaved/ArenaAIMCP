# Setup Guide

**What is this?** This guide walks you through setting up the Arena.ai MCP Server, step by step. By the end, you will have the server running locally and connected to Claude Desktop (or any MCP-compatible client).

---

## Prerequisites

Before you begin, make sure you have these installed on your machine:

- **Python 3.10 or higher** -- The project uses modern Python features. Check your version:
  ```bash
  python3 --version
  ```
  If this shows `Python 3.10.x` or higher, you are good.

- **pip** -- Python's package installer. It usually comes bundled with Python. Verify:
  ```bash
  pip3 --version
  ```

- **Git** -- To clone the repository (optional if you already have the code).

---

## Step 1: Get the code

Clone the repository to your local machine:

```bash
git clone [TODO: YOUR-REPO-URL]
cd [TODO: YOUR-PROJECT-DIRECTORY]
```

Alternatively, if you already have the project folder, navigate into it:

```bash
cd /path/to/ArenaMCPProject
```

---

## Step 2: Create a conda environment

A conda environment is an isolated folder that holds all the Python packages for this project. You create one so the packages you install here do not conflict with packages in your other projects.

```bash
conda create -n arena python=3.10
conda activate arena
```

This creates an environment called `arena` with Python 3.10. After activation, your terminal prompt should show `(arena)` at the beginning, like this:
```
(arena) your-machine:project $
```

> **Why conda?** The project requires Python 3.10+ because the MCP SDK (v1.25+) does not support older Python versions. Conda makes it easy to switch between Python versions without affecting your system Python.

---

## Step 3: Install dependencies

With the `arena` environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

This reads `requirements.txt` from the project root and installs everything the project needs: FastMCP (for the MCP server), httpx (for HTTP requests), pandas (for data handling), and others.

**Why these packages?**

| Package | Purpose |
|---|---|
| `mcp>=1.25,<2` | The Model Context Protocol library. Turns your Python functions into tools AI agents can call. Pinned below v2 to avoid breaking changes. |
| `httpx` | A modern HTTP client for Python. Ready to fetch data from the Arena.ai leaderboard in a future phase. |
| `pandas` | Organizes data into tables (DataFrames). Makes sorting and filtering easy. |
| `pytest` | Runs the automated tests. |
| `python-dotenv` | Loads environment variables from a `.env` file (for future secrets like API keys). |

---

## Step 4: Run the server for the first time

The server lives in the `src/arena_mcp/` folder. To run it, you need to tell Python where to find the project's modules by setting the `PYTHONPATH` environment variable.

From the project root directory (with your `arena` environment activated), run:

```bash
PYTHONPATH=src python src/arena_mcp/server.py
```

**What is PYTHONPATH?** It tells Python which directories to search when you `import` a module. Without it, Python would not know where `arena_client.py` is when `server.py` tries to import it.

If the server starts successfully, you will see output like:

```
INFO     Starting MCP server...
```

The server will remain running and listening for requests from your MCP client (e.g., Claude Desktop). Press `Ctrl+C` to stop it.

---

## Step 5: Verify it works with tests

Run the automated test suite to confirm everything is working:

```bash
conda activate arena
PYTHONPATH=src pytest tests/ -v
```

You should see output like:

```
tests/test_arena_client.py::test_fetch_leaderboard_returns_dataframe PASSED
tests/test_arena_client.py::test_get_top_models_returns_correct_limit PASSED
tests/test_arena_client.py::test_get_model_details_finds_existing_model PASSED
tests/test_arena_client.py::test_get_model_details_returns_none_for_an_unknown_model PASSED
tests/test_server.py::test_get_leaderboard_returns_markdown PASSED
tests/test_server.py::test_get_model_stats_found PASSED
tests/test_server.py::test_get_model_stats_not_found PASSED
tests/test_server.py::test_compare_models PASSED

============================== 8 passed in 1.37s ===============================
```

If all 8 tests pass, the code is working correctly.

---

## Step 6: Configure Claude Desktop

Claude Desktop can connect to your MCP server so you can ask questions about the AI leaderboard directly from the chat interface.

1. **Find your Claude Desktop config file location:**

   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

   If the file does not exist yet, you can create it. The parent folder should already exist (created when you installed Claude Desktop).

2. **Open the file** in a text editor.

3. **Add the following configuration** (replace `[TODO: ABSOLUTE-PATH-TO-PROJECT]` with the actual absolute path on your machine):

   ```json
   {
     "mcpServers": {
       "arena": {
         "command": "python",
         "args": [
           "[TODO: ABSOLUTE-PATH-TO-PROJECT]/src/arena_mcp/server.py"
         ],
         "env": {
           "PYTHONPATH": "[TODO: ABSOLUTE-PATH-TO-PROJECT]/src"
         }
       }
     }
   }
   ```

   **Important:** Use the full absolute path. Do not use `~` or relative paths. For example, on macOS it might look like:

   ```json
   {
     "mcpServers": {
       "arena": {
         "command": "python",
         "args": [
           "/Users/yourusername/ArenaMCPProject/src/arena_mcp/server.py"
         ],
         "env": {
           "PYTHONPATH": "/Users/yourusername/ArenaMCPProject/src"
         }
       }
     }
   }
   ```

4. **Save the file** and restart Claude Desktop completely (quit and reopen).

5. **Verify the connection:** In Claude Desktop, look for a small hammer icon (tools) or check the settings. If the server connected successfully, you should see the tools listed: `get_leaderboard`, `get_model_stats`, `compare_models`.

6. **Try a prompt:** Ask Claude something like "What are the top 5 AI models right now?" If the tools are working, Claude will call `get_leaderboard` and show you the results.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'mcp'"

**Cause:** The conda environment is not activated, or you skipped the `pip install` step.

**Fix:** Make sure your terminal shows `(arena)` in the prompt. If not, activate it:
```bash
conda activate arena
```
Then install dependencies:
```bash
pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'arena_client'" or "ImportError: attempted relative import"

**Cause:** PYTHONPATH is not set, so Python cannot find the `arena_client.py` file.

**Fix:** Make sure you are running from the project root with PYTHONPATH set:
```bash
PYTHONPATH=src python src/arena_mcp/server.py
```
Or set it permanently in your shell:
```bash
export PYTHONPATH=/absolute/path/to/project/src
```

### Server starts but Claude Desktop says "Connection failed"

**Cause:** The path in `claude_desktop_config.json` is wrong or relative.

**Fix:** Double-check the `args` path in the config file. It must be an absolute path. Also verify the `PYTHONPATH` in the `env` block is the absolute path to the `src/` directory.

### "Port in use" or "Address already in use"

**Note:** The current server uses stdio (standard input/output) transport, not HTTP, so this error should not occur in the basic setup. If you see this, you may have another server process running. Look for instructions about switching to SSE transport in future versions.

### "python: command not found"

**Cause:** Python is not installed or not on your PATH.

**Fix:** Install Python 3.10+ from python.org. On macOS, you can also use `python3` instead of `python`. If the config uses `python`, try changing it to `python3`.

### "venv: command not found"

**Cause:** The `venv` module is not available in your Python installation. On some systems (e.g., Ubuntu), you need to install it separately.

**Fix:** On Debian/Ubuntu: `sudo apt install python3-venv`. On other systems, reinstall Python with the full standard library.

### Changes to `claude_desktop_config.json` not taking effect

**Cause:** Claude Desktop caches the config file. You may need to fully quit the application (not just close the window) and reopen it.

**Fix:** On macOS, press `Cmd+Q` to fully quit Claude Desktop, then relaunch. On Windows, right-click the system tray icon and select "Quit", then reopen.

---

## Next Steps

Now that the server is running, head to the [Usage Guide](USAGE.md) to learn how to use each tool with example prompts.

If you want to understand how the code is organized, read the [Architecture Overview](ARCHITECTURE.md).
