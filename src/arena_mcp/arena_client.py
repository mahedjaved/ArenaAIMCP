"""
Client for fetching Arena.ai leaderboard data
"""

import httpx
import pandas as pd
from .schemas import ModelEntry
from typing import List, Dict, Optional


class ArenaClient:
    """
    Fetches and queries LLM leaderboard data from Arena.ai

    Currently uses mock as stable fallback.
    TODO: Implement actual API calls to Arena.ai in later phases.
    """
    MOCK_DATA = {
        "Model": [
            "gpt-4o",
            "claude-3-5-sonnet",
            "gemini-1.5-pro",
            "gpt-4-turbo",
            "llama-3-70b",
            "claude-3-opus",
            "gemini-1.5-flash",
            "mixtral-8x22b",
            "dbrx-instruct",
            "qwen-max",
        ],
        "Elo Rating": [1287, 1271, 1265, 1255, 1210, 1248, 1230, 1180, 1175, 1190],
        "Rank": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Organization": [
            "OpenAI",
            "Anthropic",
            "Google",
            "OpenAI",
            "Meta",
            "Anthropic",
            "Google",
            "Mistral",
            "Databricks",
            "Alibaba",
        ],
    }

    def __init__(self):
        self.client = httpx.Client(timeout=10.0)

    def fetch_leaderboard(self) -> pd.DataFrame:
        """
        Returns leaderboard data as a DataFrame (currently mock data)
        """
        return pd.DataFrame(self.MOCK_DATA)

    def get_top_models(self, limit: int = 10) -> List[ModelEntry]:
        """
        Returns the top N models sorted by rank.
        """
        df = self.fetch_leaderboard()
        top_df = df.sort_values(by="Rank").head(limit)
        # records are list like (e.g. ‘records’ : [{column -> value}, … , {column -> value}])
        top_df = top_df.to_dict(orient="records")
        entries = []
        for entry in top_df:
            entries.append(ModelEntry(
                model=entry['Model'], elo_rating=entry['Elo Rating'], rank=entry['Rank'], organization=entry['Organization']))
        return entries

    def get_model_details(self, model_name: str) -> Optional[ModelEntry]:
        """
        Returns details for the a specific model.
        """
        df = self.fetch_leaderboard()
        match = df[df["Model"].str.lower() == model_name.lower()]
        if not match.empty:
            match = match.iloc[0].to_dict()
            return ModelEntry(
                model=match['Model'], elo_rating=match['Elo Rating'], rank=match['Rank'], organization=match['Organization'])

        return None
