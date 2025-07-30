import sys
from datetime import datetime
import click
from rich.console import Console

from ..task_manager import TaskManager
from ..handlers.slack import SlackHandler
from ..utils.date import parse_date

console = Console()

@click.group()
def cli():
    """Daily task management CLI."""
    pass

@cli.command()
@click.option('--template-only', is_flag=True, help='Create file with template only')
@click.option('--date', type=str, help='Date in YYYY-MM-DD format')
def create(template_only: bool, date: str):
    """Create a new daily task file."""
    try:
        date_obj = parse_date(date) if date else datetime.now()
        task_manager = TaskManager()
        task_manager.create_daily_file(date_obj, template_only)
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        sys.exit(1)

@cli.command()
@click.option('--report', is_flag=True, help='Generate EOD report instead of daily plan')
@click.option('--date', type=str, help='Date in YYYY-MM-DD format')
def share(report: bool, date: str):
    """Share daily plan or EOD report."""
    try:
        date_obj = parse_date(date) if date else datetime.now()
        task_manager = TaskManager()
        tasks = task_manager.get_tasks_for_date(date_obj)
        
        # Debug output
        click.echo("\nDebug: Tasks found:")
        for project, project_tasks in tasks.items():
            click.echo(f"\n{project}:")
            for task in project_tasks:
                click.echo(f"  {task}")
        
        handler = SlackHandler()
        content = handler.format_content(tasks, date_obj, is_report=report)
        handler.send(content)
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        sys.exit(1)

@cli.group()
def config():
    """Configuration management commands."""
    pass

@config.command()
def init():
    """Initialize configuration with defaults."""
    try:
        task_manager = TaskManager()
        task_manager.init_config()
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        sys.exit(1)

@config.command()
def path():
    """Show configuration file paths."""
    try:
        task_manager = TaskManager()
        task_manager.show_config_paths()
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        sys.exit(1) 