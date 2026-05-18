"""
MCP tool definitions for the Arena leaderboard
"""

from .arena_client import ArenaClient

arena = ArenaClient()

# ToolDef 1: Get leaderboard data
def get_leaderboard(limit: int = 10) -> str:
    """
    Get the top LLMs from the Chatbot Arena leaderboard.
    :param limit: Number of models to return (default 10).
    """
    try:
        models = arena.get_top_models(limit)
        output = "# Chatbot Arena Leaderboard\n\n"
        output += "| Rank | Model | Elo | Org |\n| :--- | :--- | :--- | :--- |\n"
        for m in models:
            output += f"| {m.rank} | {m.model} | {m.elo_rating} | {m.organization} |\n"
        return output
    except Exception as e:
        return f"Error fetching leaderboard data: {str(e)}"

# ToolDef 2: Get model stats
def get_model_stats(model_name: str) -> str:
    """
    Get Elo rating and rank for a specific model.
    :param model_name: e.g. 'gpt-4o', 'claude-3-5-sonnet'
    """
    try:
        details = arena.get_model_details(model_name)
        if details:
            return (
                f"# Stats for {details.model}\n\n"
                f"- **Rank:** {details.rank}\n"
                f"- **Elo Rating:** {details.elo_rating}\n"
                f"- **Organization:** {details.organization}\n"
            )
        return f"Model '{model_name}' not found."
    except Exception as e:
        return f"Error: {str(e)}"

# ToolDef 3: Model comparison
def compare_models(model_a: str, model_b: str) -> str:
    """
    Compare two models side-by-side comparison.
    :param model_a: First model
    :param model_b: Second model 
    """
    try:
        a = arena.get_model_details(model_a)
        b = arena.get_model_details(model_b)

        if not a:
            return f"Model '{model_a}' was not found"
        if not b:
            return f"Model '{model_b}' was not found"
        
        # compute difference of Elo rating
        diff = a.elo_rating - b.elo_rating
        winner = a.model if diff > 0 else b.model

        return (
            f"# Comparison: {a.model} vs {b.model}\n\n"
            f"| Feature | {a.model} | {b.model} |\n"
            f"| :--- | :--- | :--- |\n"
            f"| Rank | {a.rank} | {b.rank} |\n"
            f"| Elo | {a.elo_rating} | {b.elo_rating} |\n"
            f"| Org | {a.organization} | {b.organization} |\n"
            f"\n**Verdict:** {winner} is ranked higher by {abs(diff)} Elo points."
        )

    except Exception as e:
        return f"Error comparing models for: {str(e)}"