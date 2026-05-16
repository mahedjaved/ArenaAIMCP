"""
MCP server for Arena.AI leaderboard tools.
"""

from mcp.server.fastmcp import FastMCP
from arena_mcp.arena_client import ArenaClient

# create the server instance and client instance
mcp = FastMCP("ArenaExplorer")
arena = ArenaClient()

# tools setup

# Tool 1: Gets latest leaderboard data
@mcp.tool()
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
            output += f"| {m['Rank']} | {m['Model']} | {m['Elo Rating']} | {m['Organization']} |\n"
        return output
    except Exception as e:
        return f"Error fetching leaderboard data: {str(e)}"
    

# Tool 2: Get model stats
@mcp.tool()
def get_model_stats(model_name: str) -> str:
    """
    Get Elo rating and rank for a specific model.
    :param model_name: e.g. 'gpt-4o', 'claude-3-5-sonnet'
    """
    try:
        details = arena.get_model_details(model_name)
        if details:
            return (
                f"# Stats for {details['Model']}\n\n"
                f"- **Rank:** {details['Rank']}\n"
                f"- **Elo Rating:** {details['Elo Rating']}\n"
                f"- **Organization:** {details['Organization']}\n"
            )
        return f"Model '{model_name}' not found."
    except Exception as e:
        return f"Error: {str(e)}"
    
# Tool 3: Compare models
@mcp.tool()
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
        diff = a["Elo Rating"] - b["Elo Rating"]
        winner = a["Model"] if diff > 0 else b["Model"]

        return (
            f"# Comparison: {a['Model']} vs {b['Model']}\n\n"
            f"| Feature | {a['Model']} | {b['Model']} |\n"
            f"| :--- | :--- | :--- |\n"
            f"| Rank | {a['Rank']} | {b['Rank']} |\n"
            f"| Elo | {a['Elo Rating']} | {b['Elo Rating']} |\n"
            f"| Org | {a['Organization']} | {b['Organization']} |\n"
            f"\n**Verdict:** {winner} is ranked higher by {abs(diff)} Elo points."
        )

    except Exception as e:
        return f"Error comparing models for: {str(e)}"
    

if __name__ == "__main__":
    mcp.run()