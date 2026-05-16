# Usage Guide

**What is this?** This guide explains how to use the three MCP tools provided by the Arena.ai server. Each section shows an example prompt, what the tool does internally, and what output to expect.

---

## Before you start

Make sure the MCP server is running and connected to your client (Claude Desktop). See the [Setup Guide](SETUP.md) for instructions.

You can ask questions in natural language. Claude will decide which tool to call based on your question.

---

## Tool 1: get_leaderboard

**What it does:** Returns the top-ranked AI models from the Chatbot Arena leaderboard, sorted by Elo rating.

**Suggested prompts:**

- "What are the top 5 AI models right now?"
- "Show me the current leaderboard"
- "Which AI model is number 1?"
- "List the top 10 models by Elo score"

**How it works:**

The tool accepts one optional parameter:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `limit` | integer | 10 | Number of top models to return |

**Expected output (markdown table):**

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

Claude will display this as a nicely formatted table in the chat.

**If no data is returned:** The server will return an error message like "Error fetching leaderboard." This usually means the data source is unreachable. The current version uses mock data, so this should not happen.

---

## Tool 2: get_model_stats

**What it does:** Looks up a specific model by name and returns its rank, Elo rating, and organization.

**Suggested prompts:**

- "How good is gpt-4o?"
- "What rank is claude-3-5-sonnet?"
- "Tell me about gemini-1.5-pro"
- "Give me the stats for llama-3-70b"

**How it works:**

The tool accepts one required parameter:

| Parameter | Type | Description |
|---|---|---|
| `model_name` | string | The name of the model (e.g., "gpt-4o", "claude-3") |

The search is **case-insensitive** and matches partial names. For example, searching "gpt" would match "gpt-4o" and "gpt-4-turbo" (but only the first match is returned).

**Expected output (formatted text with bold labels):**

```
# Stats for gpt-4o

- **Rank:** 1
- **Elo Rating:** 1287
- **Organization:** OpenAI
```

**If the model is not found:**

The server will return:

```
Model 'nonexistent-model' not found in the leaderboard.
```

**What to do:** Double-check the spelling. Model names are case-insensitive but the spelling must be close. Try a partial name like "gpt" instead of "gpt-4o-2024-05-13". If you are unsure what models exist, run `get_leaderboard` first to see the full list.

---

## Tool 3: compare_models

**What it does:** Compares two models side-by-side and declares which one is ranked higher.

**Suggested prompts:**

- "Compare gpt-4o and claude-3-5-sonnet"
- "Which is better, gemini-1.5-pro or gpt-4-turbo?"
- "How does llama-3-70b compare to mixtral-8x22b?"

**How it works:**

The tool accepts two required parameters:

| Parameter | Type | Description |
|---|---|---|
| `model_a` | string | Name of the first model |
| `model_b` | string | Name of the second model |

**Expected output (markdown table with verdict):**

```
# Comparison: gpt-4o vs claude-3-5-sonnet

| Feature | gpt-4o | claude-3-5-sonnet |
| :--- | :--- | :--- |
| Rank | 1 | 2 |
| Elo | 1287 | 1271 |
| Org | OpenAI | Anthropic |

**Verdict:** gpt-4o is currently ranked higher by 16 Elo points.
```

The verdict tells you which model has the higher Elo score and by how much.

**If one model is not found:** The server returns a message like `Model 'nonexistent' not found.` The comparison stops and does not show partial results.

---

## How to interpret Elo scores

Elo is a rating system originally designed for chess. In the Chatbot Arena, it works like this:

- **Higher Elo = better performance.** Models are ranked by their Elo score, highest first.
- **The scale is relative, not absolute.** A score of 1287 does not mean "87% accuracy." It means the model is that many points better than the baseline.
- **The gap matters.** A difference of 100 Elo points means the higher-ranked model is expected to win about 64% of head-to-head matchups. A difference of 200 points means it is expected to win about 76%.
- **Scores change over time.** As new models are added and more battles are fought, Elo ratings shift. The leaderboard is a snapshot in time.

**In the mock data:** The current version of the server uses static mock data (a predefined table of 10 models). This means every time you run a query, you get the same results. This is intentional -- it lets you test the tools without needing a live internet connection. When real Arena.ai integration is added in a future phase, the data will be live and up-to-date.

---

## Common usage patterns

### Chaining multiple queries

You can ask follow-up questions in the same conversation:

- You: "Show me the top 3 models."
- Claude: *displays leaderboard*
- You: "Compare number 1 and number 2."
- Claude: *calls `get_leaderboard` again, then `compare_models` with the two top names*

### Searching with partial names

If you are not sure of the exact name, use a partial match:

- "Tell me about gpt" -- this might match "gpt-4o" (the first model containing "gpt").
- "Stats for claude" -- this matches "claude-3-5-sonnet" (the first model containing "claude").

Note: the search returns the first match, so if multiple names contain your search term, you get the first one found.

### What to do when a tool returns an error

If any tool returns an error message (starting with "Error"), the server likely hit an unexpected problem. Try:

1. Restart the MCP server (stop it with `Ctrl+C`, then start it again).
2. Run the test script to isolate the issue:
   ```bash
   PYTHONPATH=src pytest tests/ -v
   ```
3. If the tests pass but Claude Desktop does not, check your Claude Desktop configuration (see [Setup Guide](SETUP.md#step-6-configure-claude-desktop)).

---

## Tool reference summary

| Tool | Parameters | Returns |
|---|---|---|
| `get_leaderboard` | `limit` (int, optional, default=10) | Markdown table of top models with Rank, Model, Elo, Org |
| `get_model_stats` | `model_name` (string, required) | Formatted stats: Rank, Elo, Organization |
| `compare_models` | `model_a` (string, required), `model_b` (string, required) | Side-by-side table comparison with verdict |

---

## Next steps

- Read the [Architecture Overview](ARCHITECTURE.md) to understand how these tools work under the hood.
- If you ran into any issues during setup, refer to the [Troubleshooting section](SETUP.md#troubleshooting) in the Setup Guide.
