"""
Configurations store for the Arena.AI MCP server
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Variables:
    ARENA_API_KEY = os.getenv("ARENA_API_KEY", "")
    ARENA_API_BASE_URL = os.getenv("ARENA_API_BASE_URL", "https://api.arena.ai/v1")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))