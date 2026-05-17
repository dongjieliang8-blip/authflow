"""Tests for AuthFlow pipeline."""
import pytest
from src.config import Config


def test_config_defaults():
    config = Config()
    assert config.model == "deepseek-chat"
    assert config.temperature == 0.3
    assert config.max_tokens == 4096


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setenv("DEEPSEEK_MODEL", "deepseek-coder")
    config = Config()
    assert config.api_key == "test-key"
    assert config.model == "deepseek-coder"
