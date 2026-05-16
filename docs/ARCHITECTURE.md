# Architecture Overview

**What is this?** This document explains how the Arena.ai MCP Server is organized and how data flows from your question to the leaderboard and back. It is written for a beginner who wants to understand the code without reading every line.

---

## Project layout

```
ArenaMCPProject/
  src/
    __init__.py            -- Makes src/ a Python package
    arena_mcp/
      __init__.py          -- Makes arena_mcp/ a Python package
      arena_client.py      -- Fetches and returns data (the "data layer")
      server.py            -- The MCP server entry point (registers and runs the tools)
  tests/
    __init__.py            -- Makes tests/ a Python package
    test_arena_client.py   -- Tests for the data layer
    test_server.py         -- Tests for the MCP server tools
  docs/
    SETUP.md               -- Step-by-step installation guide
    USAGE.md               -- How to use the tools with example prompts
    ARCHITECTURE.md        -- This file
  notes/
    glossary.md            -- Project jargon explained
  examples/                -- Original prototype (reference only)
  requirements.txt         -- Lists all Python packages needed
  AGENTS.md                -- Instructions for AI coding agents
```

---

## File-by-file explanation

### `src/arena_mcp/server.py` -- The MCP entry point

**Path:** `src/arena_mcp/server.py`

This is the file that MCP clients (like Claude Desktop) connect to. It uses the FastMCP library to:

1. Create an MCP server named "ArenaExplorer".
2. Register three tools (`get_leaderboard`, `get_model_stats`, `compare_models`) by decorating functions with `@mcp.tool()`.
3. Start listening for incoming requests via stdio transport.

**Why this file exists on its own:** It is the glue between the AI agent (Claude) and the data (leaderboard). It does not fetch data itself. It only defines what tools exist and what parameters they accept. This separation means you could swap out the data source without changing the tool definitions.

**Key concept -- `@mcp.tool()`:** When you add this decorator to a Python function, FastMCP automatically generates a tool description for the AI. The function's docstring becomes the tool description, and the function parameters become the tool's input fields. The AI reads these and decides when to call each tool.

### `src/arena_mcp/arena_client.py` -- The data layer

**Path:** `src/arena_mcp/arena_client.py`

This file contains the `ArenaClient` class. Its job is to provide data to the tools. It has three main methods:

- `fetch_leaderboard()` -- Returns a pandas DataFrame of all models.
- `get_top_models(limit)` -- Returns the top N models as a list of dictionaries.
- `get_model_details(model_name)` -- Returns a single model's data as a dictionary (case-insensitive exact match).

**Why separate this from server.py?** Because the data source might change. Today it uses mock data. Tomorrow it might scrape a website. Next month it might call a real API. By keeping the data logic in its own file, you can change how data is fetched without touching the tool definitions in `server.py`.

**What is the MOCK_DATA?** In `arena_client.py`, there is a dictionary called `MOCK_DATA` with 10 models, their Elo scores, ranks, and organizations. This is static data -- it never changes. We use it so beginners can test the server without needing internet access or API keys.

### `tests/` -- The automated tests

**Path:** `tests/test_arena_client.py` and `tests/test_server.py`

The project uses `pytest` for testing. There are 8 tests total:

- 4 tests for `arena_client.py` (checks DataFrame shape, return limits, model lookup, and the "not found" edge case)
- 4 tests for `server.py` (checks markdown formatting, model stats output, error handling, and comparison verdict)

Tests are run with:
```bash
PYTHONPATH=src pytest tests/ -v
```

### `requirements.txt` -- The dependency list

Every Python project needs certain external packages. This file lists them all so you can install them in one command (`pip install -r requirements.txt`). It ensures everyone on the project uses the same versions.

---

## How data flows

Here is the journey of a question from you, through the system, and back:

```
You ask: "What are the top 5 AI models?"

    1. Claude Desktop receives your message.
    2. Claude decides to call the tool get_leaderboard(limit=5).
    3. Claude sends a request through the MCP protocol (stdio) to server.py.
    4. server.py receives the request and calls the get_leaderboard function.
    5. get_leaderboard calls arena.get_top_models(5).
    6. arena.get_top_models calls fetch_leaderboard().
    7. fetch_leaderboard returns the mock data as a pandas DataFrame.
    8. get_top_models sorts by rank, takes the first 5, returns them as a list.
    9. get_leaderboard formats the list into a markdown table string.
    10. server.py sends the markdown string back to Claude via MCP (stdio).
    11. Claude displays the table in your chat window.

Total: 11 steps, but it happens in under a second.
```

```
User             Claude Desktop          MCP Server        ArenaClient
 |                     |                      |                |
 | "Top 5 models?"    |                      |                |
 |-------------------->|                      |                |
 |                     | get_leaderboard(5)   |                |
 |                     |--------------------->|                |
 |                     |                      | get_top_models |
 |                     |                      |--------------->|
 |                     |                      |                |
 |                     |                      |    DataFrame   |
 |                     |                      |<---------------|
 |                     |                      |                |
 |                     |   Markdown table     |                |
 |                     |<---------------------|                |
 |                     |                      |                |
 |   Formatted table   |                      |                |
 |<--------------------|                      |                |
```

---

## Why the separation exists

The project is split into separate files with clear responsibilities. Here is why each boundary matters:

**`arena_client.py` fetches, `server.py` registers, the tools format.**

- `arena_client.py` knows about data: where to get it, how to parse it, how to search it.
- `server.py` knows about MCP: how to register tools, how to receive requests, how to send responses.
- The tool functions in `server.py` know about formatting: they take raw data from the client and turn it into human-readable markdown.

**Why not put everything in one file?**

- **Testability:** You can test the data client independently (with `test_tools.py`) without needing an MCP client.
- **Swapability:** If Arena.ai changes their website layout, you only edit `arena_client.py`. The tool definitions stay the same.
- **Readability:** A beginner can open `server.py` and see all three tools at a glance without scrolling through HTTP parsing code.

**Does this mean more code?** Yes, slightly. But the extra files save you time when something breaks or needs to change.

---

## The mock data strategy

**What is mock data?** Fake data that looks real. The `MOCK_DATA` dictionary in `arena_client.py` contains 10 imaginary-but-realistic models with Elo scores.

**Why start with mock data instead of the real Arena.ai leaderboard?**

1. **No internet required.** You can run the server on a plane, in a coffee shop with no Wi-Fi, or on an air-gapped machine.
2. **No API keys needed.** Real data sources often require authentication, rate limiting, and error handling. Mock data removes all of that complexity for the first version.
3. **Predictable results.** The same query always returns the same answer. This makes testing and debugging much easier.
4. **You can focus on MCP.** The point of this project is to learn how MCP servers work, not to debug web scraping. Mock data removes the distraction.

**When does the real data come?** In a future phase, `fetch_leaderboard()` in `arena_client.py` will be upgraded to scrape or call the real Arena.ai API. The mock data will become a fallback (used only when the real source is unreachable). The tools in `server.py` will not change -- they do not care whether the data is real or fake.

**How does the mock data work in code?**

```python
MOCK_DATA = {
    "Model": ["gpt-4o", "claude-3-5-sonnet", ...],
    "Elo Rating": [1287, 1271, ...],
    "Rank": [1, 2, ...],
    "Organization": ["OpenAI", "Anthropic", ...]
}
```

This dictionary is converted to a pandas DataFrame when `fetch_leaderboard()` is called. The DataFrame is then sorted and filtered by `get_top_models()` and `get_model_details()`. Because all operations use pandas, switching to a live data source later is straightforward -- just change what `fetch_leaderboard()` returns.

---

## How the three tools relate to each other

```
get_leaderboard(limit)
    |
    |-- Uses: get_top_models(limit)
    |-- Returns: table of N models
    |-- Purpose: Overview of the whole leaderboard

get_model_stats(model_name)
    |
    |-- Uses: get_model_details(model_name)
    |-- Returns: details for one model
    |-- Purpose: Deep dive on a single model

compare_models(model_a, model_b)
    |
    |-- Uses: get_model_details(model_a), get_model_details(model_b)
    |-- Returns: comparison table + verdict
    |-- Purpose: Head-to-head between two models
```

All three tools use the same underlying `ArenaClient` instance, which means they all read from the same data source. If the data source changes (e.g., from mock to live), all three tools automatically use the new data.

---

## What comes next (future phases)

The MVP is complete with `src/arena_mcp/` and `tests/`. Future additions may include:

- **`tools.py`** -- Tool function definitions separated from `server.py` for cleaner organization (currently the tools are inline in `server.py`).
- **`schemas.py`** -- Pydantic models that validate tool inputs (e.g., ensuring `model_name` is a non-empty string).
- **`config.py`** -- Centralized configuration (timeouts, URLs, API keys) loaded from environment variables.
- **Live data fetching** -- `fetch_leaderboard()` will make real HTTP requests to Arena.ai (via HuggingFace dataset `lmarena-ai/leaderboard-dataset`) instead of returning mock data.
- **HTTP transport** -- The server may support HTTP/SSE in addition to stdio, allowing remote connections.

The project is designed to grow into these additions naturally. Each new piece fits into the existing separation of concerns without requiring a rewrite.
