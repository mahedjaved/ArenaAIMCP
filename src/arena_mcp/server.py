"""
MCP server for Arena.AI leaderboard tools.
"""

from mcp.server.fastmcp import FastMCP
from .tools import *

# create the server instance and client instance
mcp = FastMCP("ArenaExplorer")

# tools setup

# Tool 1: Gets latest leaderboard data
mcp.tool()(get_leaderboard)
   
# Tool 2: Get model stats
mcp.tool()(get_model_stats)
   
# Tool 3: Compare models
mcp.tool()(compare_models)
 

if __name__ == "__main__":
    mcp.run()