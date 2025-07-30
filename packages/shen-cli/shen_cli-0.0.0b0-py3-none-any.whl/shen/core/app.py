"""Main application class for Shen."""


from shen import __version__
from shen.core.config import Config
from shen.core.plugin_manager import PluginManager


class ShenApp:
    """Main application class that coordinates all components."""

    def __init__(self, debug: bool = False) -> None:
        """Initialize the Shen application.

        Args:
            debug: Enable debug mode
        """
        self.debug = debug
        self.config = Config()
        self.plugin_manager = PluginManager()
        self._initialize()

    def _initialize(self) -> None:
        """Initialize the application components."""
        # Load configuration
        self.config.load()

        # Initialize plugin manager
        self.plugin_manager.discover_plugins()

    def get_info(self) -> str:
        """Get information about Shen and its capabilities.

        Returns:
            Formatted information string
        """
        info_lines = [
            f"[bold]Shen v{__version__}[/bold]",
            "",
            "[cyan]Capabilities:[/cyan]",
            "• Document organization and management",
            "• System cleanup and maintenance",
            "• Office document creation",
            "• Security checks",
            "• Information retrieval",
            "• Task automation",
            "",
            f"[cyan]Plugins loaded:[/cyan] {len(self.plugin_manager.plugins)}",
            f"[cyan]Debug mode:[/cyan] {'Enabled' if self.debug else 'Disabled'}",
        ]

        return "\n".join(info_lines)

    def run_task(self, task: str, interactive: bool = False) -> str:
        """Run a task based on natural language input.

        Args:
            task: Natural language task description
            interactive: Whether to run in interactive mode

        Returns:
            Task execution result
        """
        # This is a placeholder implementation
        # In a real implementation, this would:
        # 1. Parse the task using NLP
        # 2. Determine which plugin(s) to use
        # 3. Execute the task
        # 4. Return formatted results

        if interactive:
            return f"[yellow]Interactive mode not yet implemented.[/yellow]\n\nTask: {task}"
        else:
            return f"[yellow]Task execution not yet implemented.[/yellow]\n\nTask: {task}"

    def list_plugins(self) -> str:
        """List all available plugins and their capabilities.

        Returns:
            Formatted plugin information
        """
        if not self.plugin_manager.plugins:
            return (
                "[yellow]No plugins currently available.[/yellow]\n\n"
                "Plugins will be added in future versions."
            )

        # This would list actual plugins when implemented
        return "[yellow]Plugin system under development.[/yellow]"
