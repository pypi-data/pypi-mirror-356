"""CLI entry point for Shen."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from shen import __version__
from shen.core.app import ShenApp
from shen.utils.logging import setup_logging

console = Console()


@click.group(invoke_without_command=True)
@click.option(
    "--version",
    "-v",
    is_flag=True,
    help="Show version and exit.",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode.",
)
@click.pass_context
def cli(ctx: click.Context, version: bool, debug: bool) -> None:
    """Shen - Your AI assistant for daily non-programming tasks.

    Shen helps you automate various daily tasks such as:
    - Document organization and management
    - System cleanup and maintenance
    - Office document creation
    - Security checks
    - And more!
    """
    if version:
        console.print(f"Shen version {__version__}")
        ctx.exit()

    if ctx.invoked_subcommand is None:
        # Show welcome message when no command is provided
        welcome_text = Text.from_markup(
            "[bold cyan]Shen[/bold cyan] - Your AI assistant for daily tasks\n\n"
            f"Version: {__version__}\n"
            "Type 'shen --help' to see available commands."
        )
        console.print(Panel(welcome_text, title="Welcome", border_style="cyan"))

    # Setup logging
    setup_logging(debug=debug)

    # Initialize app context
    ctx.ensure_object(dict)
    ctx.obj["app"] = ShenApp(debug=debug)


@cli.command()
@click.pass_context
def info(ctx: click.Context) -> None:
    """Show information about Shen and its capabilities."""
    app: ShenApp = ctx.obj["app"]
    info_text = app.get_info()
    console.print(Panel(info_text, title="Shen Information", border_style="green"))


@cli.command()
@click.argument("task", type=str)
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Run in interactive mode.",
)
@click.pass_context
def run(ctx: click.Context, task: str, interactive: bool) -> None:
    """Run a task or command.

    Examples:
        shen run "organize my downloads folder"
        shen run "check system security" --interactive
    """
    app: ShenApp = ctx.obj["app"]

    with console.status(f"Processing: {task}", spinner="dots"):
        try:
            result = app.run_task(task, interactive=interactive)
            console.print(Panel(result, title="Task Result", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
            ctx.exit(1)


@cli.command()
@click.pass_context
def plugins(ctx: click.Context) -> None:
    """List available plugins and their capabilities."""
    app: ShenApp = ctx.obj["app"]
    plugins_info = app.list_plugins()
    console.print(Panel(plugins_info, title="Available Plugins", border_style="blue"))


def main() -> None:
    """Main entry point."""
    cli(obj={})


if __name__ == "__main__":
    main()
