import click
from datetime import datetime
from typing import Optional
from pathlib import Path

from ..task_manager import TaskManager
from ..handlers.slack import SlackHandler
from ..utils import parse_date
from .. import config_manager
from ..config_manager import get_config

@click.group()
def main():
    """Daily Task Template - A template for daily task and note management system."""
    pass

@main.command()
@click.option('--date', '-d', help='Date in YYYY-MM-DD format (default: today)')
@click.option('--template-only', is_flag=True, help='Create file without carrying forward tasks')
def create(date: str, template_only: bool):
    """Create a new daily file."""
    date_obj = parse_date(date) if date else datetime.now()
    task_manager = TaskManager()
    task_manager.create_daily_file(date_obj, template_only=template_only)

@main.command()
@click.option('--date', '-d', help='Date in YYYY-MM-DD format (default: today)')
@click.option('--report/--plan', default=False, help='Generate EOD report instead of planning message')
@click.option('--output-type', '-t', default='slack', type=click.Choice(['slack']), help='Output type')
@click.option('--no-copy', is_flag=True, help='Do not copy to clipboard')
def share(date: str, report: bool, output_type: str, no_copy: bool):
    """Share daily tasks through various channels."""
    date_obj = parse_date(date) if date else datetime.now()
    task_manager = TaskManager()
    tasks = task_manager.get_tasks_for_date(date_obj)

    # Get appropriate handler based on output type
    handlers = {
        'slack': SlackHandler,
        # Add more handlers here as they are implemented
        # 'email': EmailHandler,
        # 'notion': NotionHandler,
        # 'gdrive': GoogleDriveHandler,
    }

    handler_class = handlers.get(output_type)
    if not handler_class:
        click.echo(f"Error: Unsupported output type '{output_type}'")
        return

    handler = handler_class()
    content = handler.format_content(tasks, date_obj, is_report=report)
    
    if not no_copy:
        handler.send(content)
    click.echo(content)

@main.command()
@click.option('--start-date', '-s', help='Start date in YYYY-MM-DD format')
@click.option('--end-date', '-e', help='End date in YYYY-MM-DD format')
def stats(start_date: Optional[str], end_date: Optional[str]):
    """Show statistics for the specified date range."""
    click.echo("Stats functionality to be implemented")

@main.group()
def config():
    """Manage configuration settings."""
    pass

@config.command()
def init():
    """Initialize or reset user configuration to defaults."""
    config_manager.reset_to_defaults()
    click.echo("Configuration initialized with default settings.")
    click.echo(f"Config file: {config_manager.USER_CONFIG_FILE}")
    click.echo(f"Template file: {config_manager.USER_TEMPLATE_FILE}")

@config.command()
def path():
    """Show paths to configuration files."""
    click.echo(f"User config directory: {config_manager.USER_CONFIG_DIR}")
    click.echo(f"Config file: {config_manager.USER_CONFIG_FILE}")
    click.echo(f"Template file: {config_manager.USER_TEMPLATE_FILE}")
    click.echo(f"\nDefault config directory: {config_manager.DEFAULT_CONFIG_DIR}")

@main.command()
@click.argument('task_name')
@click.option('--category', help='Task category (Personal/Work/Learning)')
def complete(task_name: str, category: str):
    """Mark a task as complete."""
    date_obj = datetime.now()
    task_manager = TaskManager()
    success = task_manager.complete_task(task_name, category, date_obj)
    if success:
        click.echo(f"✅ Task '{task_name}' marked as complete.")
    else:
        click.echo(f"❌ Task '{task_name}' not found in category '{category}'.")

@main.command()
def share_today():
    """Share today's tasks."""
    date_obj = datetime.now()
    task_manager = TaskManager()
    tasks = task_manager.get_tasks_for_date(date_obj)
    
    # Get handler based on config
    config = get_config()
    handler = SlackHandler()
    
    # Format and share tasks
    handler.share_tasks(tasks)
    click.echo("✓ Message copied to clipboard!")

@config.group()
def config_group():
    """Configuration commands group."""
    pass

@config_group.command(name='init')
def config_init():
    """Initialize configuration with default settings."""
    task_manager.init_config()

@config_group.command(name='path')
def config_path():
    """Show configuration paths."""
    task_manager.show_config_paths()

if __name__ == '__main__':
    main() 