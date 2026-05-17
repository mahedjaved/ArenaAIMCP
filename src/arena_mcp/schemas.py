"""
Purpose of this code is to set the Pydantic schema representing a model entry from the Chatbot Arena leaderboard
"""

from pydantic import BaseModel


class ModelEntry(BaseModel):
    model: str
    elo_rating: int
    rank: int
    organization: str