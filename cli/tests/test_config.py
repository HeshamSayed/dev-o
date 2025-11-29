"""
Tests for configuration management.
"""
import pytest
import tempfile
import os
from pathlib import Path

from ..config import ConfigManager, UserConfig


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create temporary config directory."""
    config_dir = tmp_path / ".devo"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def config_manager(temp_config_dir, monkeypatch):
    """Create config manager with temp directory."""
    manager = ConfigManager()
    monkeypatch.setattr(manager, "config_dir", temp_config_dir)
    monkeypatch.setattr(manager, "config_file", temp_config_dir / "config.json")
    return manager


def test_config_manager_init(config_manager):
    """Test config manager initialization."""
    assert config_manager.config_dir.exists()


def test_load_user_config_creates_default(config_manager):
    """Test loading user config creates default if not exists."""
    config = config_manager.load_user_config()

    assert isinstance(config, UserConfig)
    assert config.api_url == "http://localhost:8000"
    assert config.preferred_llm == "deepseek-r1:7b"


def test_save_and_load_user_config(config_manager):
    """Test saving and loading user config."""
    # Create and save config
    config = UserConfig(
        email="test@example.com",
        api_url="http://test:8000",
        preferred_llm="test-model",
    )

    config_manager.save_user_config(config)

    # Load config
    loaded_config = config_manager.load_user_config()

    assert loaded_config.email == "test@example.com"
    assert loaded_config.api_url == "http://test:8000"
    assert loaded_config.preferred_llm == "test-model"


def test_get_set_config_values(config_manager):
    """Test getting and setting config values."""
    # Set value
    config_manager.set("preferred_llm", "new-model")

    # Get value
    value = config_manager.get("preferred_llm")

    assert value == "new-model"


def test_get_unknown_key_returns_default(config_manager):
    """Test getting unknown key returns default."""
    value = config_manager.get("unknown_key", "default_value")

    assert value == "default_value"


def test_set_unknown_key_raises_error(config_manager):
    """Test setting unknown key raises error."""
    with pytest.raises(KeyError):
        config_manager.set("unknown_key", "value")


def test_list_all_config(config_manager):
    """Test listing all config."""
    all_config = config_manager.list_all()

    assert isinstance(all_config, dict)
    assert "api_url" in all_config
    assert "preferred_llm" in all_config


def test_reset_config(config_manager):
    """Test resetting config."""
    # Set custom values
    config_manager.set("preferred_llm", "custom-model")

    # Reset
    config_manager.reset()

    # Check defaults
    config = config_manager.load_user_config()
    assert config.preferred_llm == "deepseek-r1:7b"
