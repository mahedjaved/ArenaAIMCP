# Glossary — ArenaMCP Project

## Elo Score (Elo Rating)

A **comparison-based rating system**, originally from chess, now used in video games and LLM leaderboards.

**How it works:**
- Two models battle head-to-head in blind comparisons
- Human judges vote on which response is better
- If Model A (rated 1200) beats Model B (rated 1100), A **gains** points and B **loses** points
- If the *underdog* wins, the point swing is larger
- If the *favorite* wins, the swing is smaller

**In our leaderboard:**
A higher Elo means the model is more likely to win against lower-ranked opponents.

| Model | Elo | Meaning |
|---|---|---|
| gpt-4o | 1287 | Top dog — wins most matchups |
| claude-3-5-sonnet | 1271 | Close competitor |
| dbrx-instruct | 1175 | Trailing, but competitive |

A gap of ~100 points means the higher-ranked model wins roughly **65%** of the time.
