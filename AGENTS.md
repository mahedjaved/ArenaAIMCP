# ArenaMCP Project

Python MCP server for Arena.ai integration and leaderboard-style workflow access.

## Project goals
- Build a beginner-friendly Python MCP server.
- Keep MCP logic separate from HTTP/client logic.
- Use the `examples/` folder as the reference implementation area.
- Start with a small MVP and grow in phases.
- Prefer simple, readable code over clever abstractions.

## Stack
- Python 3.10+
- FastMCP / `mcp>=1.0.0`
- `httpx`
- `pydantic`
- `beautifulsoup4`
- `pandas`
- `pytest`
- `pytest-asyncio`
- `ruff`
- `black`
- Optional: `python-dotenv`, `tenacity`, `mypy`
- Transport: stdio first, HTTP/SSE later if needed

## Repository layout
- `examples/` — prototype implementation, reference outputs, and earlier agent work
- `src/` — production code to be created next
- `tests/` — automated tests
- `docs/` — design notes and usage docs
- `AGENTS.md` — project instructions for all coding agents

## Working rules
- Always read the relevant files in `examples/` before changing implementation code.
- Treat `examples/` as the current reference point unless the user asks to replace it.
- Keep each file focused on one responsibility.
- Use explicit types and schema validation where helpful.
- Keep tool outputs concise and LLM-friendly.
- Prefer environment variables for all secrets and runtime configuration.
- Do not hardcode API keys, tokens, or local machine paths.

## Build philosophy
- Build the smallest useful version first.
- Avoid premature abstraction.
- Separate concerns clearly:
  - `server.py` for MCP entrypoint and tool registration
  - `arena_client.py` for Arena.ai HTTP/API integration
  - `schemas.py` for Pydantic models
  - `config.py` for environment and settings
  - `tools.py` for MCP tool definitions
- If a decision affects architecture, document it before coding.

## Beginner support rules
- Explain concepts in plain English first.
- When teaching, always explain why a step matters.
- Break work into very small coding steps.
- If the user is unsure, recommend the safest simple approach.
- Do not assume MCP knowledge.

## Agent workflow
### 1. Repo reading
- Start by reading `examples/`.
- Summarize what exists, what is missing, and what should be reused.

### 2. Planning
- Break the project into phases.
- Identify the next smallest coding step.
- Note dependencies and risks.

### 3. Implementation
- Make one focused change at a time.
- Keep code consistent with the reference examples.
- Favor clear code over compressed code.

### 4. Review
- Check style, correctness, schema design, and security.
- Compare against `examples/`.
- Flag overengineering and beginner-unfriendly complexity.

### 5. Testing
- Add tests for every meaningful change.
- Test success paths and failure paths.
- Keep tests easy to run locally.

### 6. Documentation
- Update docs when behavior changes.
- Keep setup instructions short and accurate.
- Include example prompts and commands.

## Commands
```bash
# install
python -m venv venv && source venv/bin/activate && pip install -r examples/requirements.txt

# run server
PYTHONPATH=examples python examples/server.py

# test client
python examples/test_tools.py

# run tests
pytest
```

## Current state
- Prototype lives in `examples/`.
- Root production package still needs to be created.
- Prototype currently uses mock data / static DataFrame fallback.
- Real Arena.ai integration can be added in later phases.

## Tools
| Tool | What it does |
|---|---|
| `get_leaderboard(limit)` | Top N models by Elo |
| `get_model_stats(model_name)` | Elo + rank for a model |
| `compare_models(model_a, model_b)` | Side-by-side comparison |

## Claude Desktop config
```json
{
  "mcpServers": {
    "arena": {
      "command": "python",
      "args": ["/abs/path/to/src/server.py"],
      "env": {
        "PYTHONPATH": "/abs/path/to/project"
      }
    }
  }
}
```

## Decision log
- Keep stdio as the first transport.
- Keep mock fallback until real Arena.ai access is verified.
- Add real scraping or API integration only after the MVP is stable.