"""
Tests for the ArenaClient data layer.
"""

import pytest
import pandas as pd
from arena_mcp.arena_client import ArenaClient

# Test 1: Fetch leaderboard data (Data Layer)
def test_fetch_leaderboard_returns_dataframe():
    client = ArenaClient()
    df = client.fetch_leaderboard()
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["Model", "Elo Rating", "Rank", "Organization"]
    assert len(df) == 10

# Test 2: Test Get Top Models Rerutns Correct Limit
def test_get_top_models_returns_correct_limit():
    """Getting top 3 models should return the correct number"""
    client = ArenaClient()
    result = client.get_top_models(3)
    assert len(result) == 3
    assert result[0].rank == 1  # Rank 1 for the best model

# Test 3: Test Get Models Details Finds Existing Model
def test_get_model_details_finds_existing_model():
    """Example getting details on model 'gpt-4o' should return the correct data"""
    client = ArenaClient()
    result = client.get_model_details("gpt-4o")
    assert result is not None
    assert result.model == "gpt-4o"
    assert result.elo_rating == 1287
    assert result.rank == 1

# Test 4: Test Get Model Details Returns None For Unknown
def test_get_model_details_returns_none_for_an_unknown_model():
    """Get model details should return None for a model not in the data."""
    client = ArenaClient()
    result = client.get_model_details("nonexistent-model-9XXXX")
    assert result is None