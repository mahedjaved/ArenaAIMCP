"""
Tests for the MCP server tools.
"""

import pytest
from arena_mcp.server import get_leaderboard, get_model_stats, compare_models

# Test 1: Getting leaderboard returns a markdown
def test_get_leaderboard_returns_markdown():
    """get_leaderboard should return a markdown table."""
    result = get_leaderboard(3)
    assert result.startswith("# Chatbot Arena Leaderboard")
    assert "| Rank | Model | Elo | Org |" in result
    assert "gpt-4o" in result
    assert "1287" in result

# Test 2: Get stats for a single model
def test_get_model_stats_found():
    """get_model_stats should return stats for an existing model."""
    result = get_model_stats("gpt-4o")
    assert result.startswith("# Stats for gpt-4o")
    assert "**Rank:** 1" in result
    assert "**Elo Rating:** 1287" in result


# Test 3: Get stats for an unknown model returns not found
def test_get_model_stats_not_found():
    """get_model_stats should return error message for unknown model."""
    result = get_model_stats("made-up-model")
    assert "not found" in result.lower()


# Test 4: Get difference between Elo for gpt-4o vs claude-3-5-sonnet
def test_compare_models():
    """compare_models should show side-by-side comparison with a verdict."""
    result = compare_models("gpt-4o", "claude-3-5-sonnet")
    assert "Comparison:" in result
    assert "gpt-4o" in result
    assert "claude-3-5-sonnet" in result
    assert "Verdict:" in result
    assert "16" in result  # Elo difference