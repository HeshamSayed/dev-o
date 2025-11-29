"""
Configuration management for DEVO CLI.

Handles user settings, API credentials, and project preferences.
"""
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class CLIConfig(BaseSettings):
    """CLI configuration from environment variables."""

    # API Configuration
    api_url: str = Field(default="https://backend.devtools-co.com", env="DEVO_API_URL")
    api_key: Optional[str] = Field(default=None, env="DEVO_API_KEY")

    # LLM Configuration
    preferred_llm: str = Field(default="deepseek-r1:7b", env="DEVO_PREFERRED_LLM")

    # User Preferences
    timezone: str = Field(default="UTC", env="DEVO_TIMEZONE")

    # CLI Settings
    verbose: bool = Field(default=False, env="DEVO_VERBOSE")
    color: bool = Field(default=True, env="DEVO_COLOR")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class UserConfig(BaseModel):
    """User-specific configuration stored in config file."""

    # User Identity
    email: Optional[str] = None
    username: Optional[str] = None

    # API Settings
    api_url: str = "https://backend.devtools-co.com"
    api_key: Optional[str] = None

    # Project Settings
    default_project_id: Optional[str] = None
    last_project_id: Optional[str] = None

    # LLM Settings
    preferred_llm: str = "deepseek-r1:7b"

    # UI Settings
    theme: str = "dark"
    show_thinking: bool = True
    show_tool_calls: bool = True
    compact_mode: bool = False

    # Other Settings
    timezone: str = "UTC"
    auto_checkpoint: bool = True
    checkpoint_interval: int = 300  # seconds


class ConfigManager:
    """Manages CLI configuration storage and retrieval."""

    def __init__(self):
        self.config_dir = Path.home() / ".devo"
        self.config_file = self.config_dir / "config.json"
        self.env_config = CLIConfig()
        self._user_config: Optional[UserConfig] = None

    def ensure_config_dir(self) -> None:
        """Ensure configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_user_config(self) -> UserConfig:
        """Load user configuration from file."""
        if self._user_config is not None:
            return self._user_config

        self.ensure_config_dir()

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                self._user_config = UserConfig(**data)
            except Exception as e:
                # If config is corrupted, create new one
                self._user_config = UserConfig()
        else:
            self._user_config = UserConfig()

        return self._user_config

    def save_user_config(self, config: Optional[UserConfig] = None) -> None:
        """Save user configuration to file."""
        if config is None:
            config = self._user_config

        if config is None:
            return

        self.ensure_config_dir()

        with open(self.config_file, 'w') as f:
            json.dump(config.model_dump(), f, indent=2)

        self._user_config = config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        user_config = self.load_user_config()

        # Check user config first
        if hasattr(user_config, key):
            return getattr(user_config, key)

        # Then check environment config
        if hasattr(self.env_config, key):
            return getattr(self.env_config, key)

        return default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        user_config = self.load_user_config()

        if hasattr(user_config, key):
            setattr(user_config, key, value)
            self.save_user_config(user_config)
        else:
            raise KeyError(f"Unknown configuration key: {key}")

    def get_api_url(self) -> str:
        """Get API URL (environment takes precedence)."""
        if self.env_config.api_url != "https://backend.devtools-co.com":
            return self.env_config.api_url
        return self.get("api_url", "https://backend.devtools-co.com")

    def get_api_key(self) -> Optional[str]:
        """Get API key (environment takes precedence)."""
        if self.env_config.api_key:
            return self.env_config.api_key
        return self.get("api_key")

    def set_api_key(self, api_key: str) -> None:
        """Set API key."""
        self.set("api_key", api_key)

    def get_project_dir(self, project_id: Optional[str] = None) -> Path:
        """Get project working directory."""
        if project_id is None:
            project_id = self.get("last_project_id")

        if project_id is None:
            raise ValueError("No project ID provided and no last project set")

        project_dir = self.config_dir / "projects" / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir

    def list_all(self) -> Dict[str, Any]:
        """List all configuration values."""
        user_config = self.load_user_config()
        return user_config.model_dump()

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self._user_config = UserConfig()
        self.save_user_config()


# Global config instance
config = ConfigManager()
