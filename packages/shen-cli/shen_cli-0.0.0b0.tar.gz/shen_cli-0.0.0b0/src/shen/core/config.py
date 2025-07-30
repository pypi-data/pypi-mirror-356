"""Configuration management for Shen."""

import json
from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings


class ShenSettings(BaseSettings):
    """Application settings using pydantic."""

    debug: bool = Field(default=False, description="Enable debug mode")
    plugin_dirs: list[str] = Field(
        default_factory=lambda: ["~/.shen/plugins"], description="Directories to search for plugins"
    )
    mcp_enabled: bool = Field(
        default=False, description="Enable MCP (Model Context Protocol) integration"
    )

    model_config = {
        "env_prefix": "SHEN_",
        "env_file": ".env",
    }


class Config:
    """Configuration manager for Shen."""

    def __init__(self) -> None:
        """Initialize configuration."""
        self.config_dir = Path.home() / ".shen"
        self.config_file = self.config_dir / "config.json"
        self.settings = ShenSettings()
        self._user_config: dict[str, Any] = {}

    def load(self) -> None:
        """Load configuration from file."""
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Load user configuration if it exists
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    self._user_config = json.load(f)
            except json.JSONDecodeError:
                # Handle corrupted config file
                self._user_config = {}

    def save(self) -> None:
        """Save configuration to file."""
        # Ensure config directory exists before saving
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self._user_config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        # First check user config, then settings, then default
        if key in self._user_config:
            return self._user_config[key]
        elif hasattr(self.settings, key):
            return getattr(self.settings, key)
        else:
            return default

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._user_config[key] = value
        self.save()
