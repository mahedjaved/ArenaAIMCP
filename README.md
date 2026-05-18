# ArenaAI MCP Server 🏆

**A Model Context Protocol (MCP) server for the Chatbot Arena leaderboard.**

Query top LLMs, compare Elo ratings, and explore model rankings — all from your MCP-compatible client (Claude Desktop, VS Code, etc.).

---

## ✨ Features

| Tool | Description |
|---|---|
| `get_leaderboard(limit)` | Top N models by Elo rating |
| `get_model_stats(model_name)` | Rank, Elo, and org for a specific model |
| `compare_models(model_a, model_b)` | Side-by-side comparison with a verdict |

```
# Chatbot Arena Leaderboard
| Rank | Model | Elo | Org |
| :--- | :--- | :--- | :--- |
| 1 | gpt-4o | 1287 | OpenAI |
| 2 | claude-3-5-sonnet | 1271 | Anthropic |
| 3 | gemini-1.5-pro | 1265 | Google |
```

---

## 🏗️ Architecture

```
src/arena_mcp/
├── server.py         # MCP entrypoint & tool registration
├── tools.py          # MCP tool definitions (3 tools)
├── arena_client.py   # Data fetching & API integration layer
├── schemas.py        # Pydantic data models (ModelEntry)
├── config.py         # Environment variables & settings
└── __init__.py
```

Each file has one responsibility — MCP concerns stay separate from HTTP/client logic.

---

## 🚀 Quick Start

```bash
# 1. Clone & enter
git clone https://github.com/mahedjaved/ArenaAIMCP.git
cd ArenaAIMCP

# 2. Create virtual environment
python3 -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests
pytest

# 5. Start the MCP server
PYTHONPATH=src python src/arena_mcp/server.py
```

---

## 🧪 Test Results

```
================================ test session starts =================================
platform darwin -- Python 3.12.8, pytest-9.0.3, pluggy-1.6.0
collected 8 items

tests/test_arena_client.py::test_fetch_leaderboard_returns_dataframe PASSED [ 12%]
tests/test_arena_client.py::test_get_top_models_returns_correct_limit    PASSED [ 25%]
tests/test_arena_client.py::test_get_model_details_finds_existing_model  PASSED [ 37%]
tests/test_arena_client.py::test_get_model_details_returns_none_for_unknown PASSED [ 50%]
tests/test_server.py::test_get_leaderboard_returns_markdown              PASSED [ 62%]
tests/test_server.py::test_get_model_stats_found                         PASSED [ 75%]
tests/test_server.py::test_get_model_stats_not_found                     PASSED [ 87%]
tests/test_server.py::test_compare_models                                PASSED [100%]

============================== 8 passed in 1.48s =================================
```

---

## 🛠️ Tool Examples

### Leaderboard

```bash
PYTHONPATH=src python -c "
from arena_mcp.tools import get_leaderboard
print(get_leaderboard(5))
"
```

Output:
```
# Chatbot Arena Leaderboard

| Rank | Model | Elo | Org |
| :--- | :--- | :--- | :--- |
| 1 | gpt-4o | 1287 | OpenAI |
| 2 | claude-3-5-sonnet | 1271 | Anthropic |
| 3 | gemini-1.5-pro | 1265 | Google |
| 4 | gpt-4-turbo | 1255 | OpenAI |
| 5 | llama-3-70b | 1210 | Meta |
```

### Model Stats

```bash
PYTHONPATH=src python -c "
from arena_mcp.tools import get_model_stats
print(get_model_stats('gpt-4o'))
"
```

Output:
```
# Stats for gpt-4o

- **Rank:** 1
- **Elo Rating:** 1287
- **Organization:** OpenAI
```

### Model Comparison

```bash
PYTHONPATH=src python -c "
from arena_mcp.tools import compare_models
print(compare_models('gpt-4o', 'claude-3-5-sonnet'))
"
```

Output:
```
# Comparison: gpt-4o vs claude-3-5-sonnet

| Feature | gpt-4o | claude-3-5-sonnet |
| :--- | :--- | :--- |
| Rank | 1 | 2 |
| Elo | 1287 | 1271 |
| Org | OpenAI | Anthropic |

**Verdict:** gpt-4o is ranked higher by 16 Elo points.
```

---

## ⚙️ Configuration

Copy `.env.example` to `.env` and adjust:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `ARENA_API_KEY` | `""` | API key for Arena.ai (future use) |
| `ARENA_API_BASE_URL` | `https://api.arena.ai/v1` | API base URL |
| `REQUEST_TIMEOUT` | `30` | HTTP request timeout in seconds |

---

## 🖥️ Claude Desktop Setup

Add this to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "arena": {
      "command": "python",
      "args": ["/absolute/path/to/src/arena_mcp/server.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/project/src"
      }
    }
  }
}
```

---

## 🗺️ Next Steps

- [ ] Replace mock data with live Arena.ai scraping
- [ ] Wire config into arena_client.py
- [ ] Add more tools (search by org, filtered queries)
- [ ] Add HTTP/SSE transport
- [ ] CI with GitHub Actions

---

## 📄 License

MIT
