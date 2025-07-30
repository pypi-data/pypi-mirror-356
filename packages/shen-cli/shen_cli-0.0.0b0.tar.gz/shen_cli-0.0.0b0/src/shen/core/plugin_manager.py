"""Plugin management system for Shen."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class Plugin(ABC):
    """Base class for all Shen plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description."""
        pass

    @property
    @abstractmethod
    def capabilities(self) -> list[str]:
        """List of capabilities this plugin provides."""
        pass

    @abstractmethod
    def can_handle(self, task: str) -> bool:
        """Check if this plugin can handle the given task.

        Args:
            task: Task description

        Returns:
            True if plugin can handle the task
        """
        pass

    @abstractmethod
    def execute(self, task: str, **kwargs: Any) -> dict[str, Any]:
        """Execute a task.

        Args:
            task: Task description
            **kwargs: Additional arguments

        Returns:
            Execution result
        """
        pass


class PluginManager:
    """Manages plugins for Shen."""

    def __init__(self) -> None:
        """Initialize plugin manager."""
        self.plugins: dict[str, Plugin] = {}

    def discover_plugins(self) -> None:
        """Discover and load available plugins."""
        # This is a placeholder for plugin discovery
        # In a real implementation, this would:
        # 1. Search plugin directories
        # 2. Load plugin modules
        # 3. Register plugin instances
        pass

    def register_plugin(self, plugin: Plugin) -> None:
        """Register a plugin.

        Args:
            plugin: Plugin instance to register
        """
        self.plugins[plugin.name] = plugin

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get a plugin by name.

        Args:
            name: Plugin name

        Returns:
            Plugin instance or None
        """
        return self.plugins.get(name)

    def find_plugins_for_task(self, task: str) -> list[Plugin]:
        """Find plugins that can handle a given task.

        Args:
            task: Task description

        Returns:
            List of capable plugins
        """
        capable_plugins = []
        for plugin in self.plugins.values():
            if plugin.can_handle(task):
                capable_plugins.append(plugin)
        return capable_plugins
