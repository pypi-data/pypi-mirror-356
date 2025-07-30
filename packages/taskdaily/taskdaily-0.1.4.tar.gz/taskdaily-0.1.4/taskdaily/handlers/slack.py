from datetime import datetime
from typing import Dict, Any
import pyperclip
from rich import print as rprint

from .base import OutputHandler
from .formatters.slack_formatter import SlackFormatter
from ..utils import get_status_info

class SlackHandler(OutputHandler):
    """Handler for Slack message formatting and clipboard operations."""
    
    def __init__(self):
        self.status_info = get_status_info()
        self.formatter = SlackFormatter(self.status_info)

    def format_content(self, tasks: Dict[str, Any], date: datetime, is_report: bool = False) -> str:
        """Format tasks for Slack message."""
        return self.formatter.format_message(tasks, date, is_report)

    def send(self, content: str, **kwargs) -> bool:
        """Copy content to clipboard and display preview."""
        try:
            pyperclip.copy(content)
            rprint("\n[bold]Preview of Slack message:[/bold]")
            rprint(content)
            rprint("\n[green]✓[/green] Message copied to clipboard!")
            return True
        except Exception as e:
            rprint(f"[red]✗[/red] Failed to copy to clipboard: {e}")
            return False

    def _convert_to_slack_format(self, task: str) -> str:
        """Convert markdown task format to Slack format."""
        # Remove markdown checkbox
        task = task.replace("- [ ]", "•").replace("- [x]", "✓")
        
        # Convert status emojis
        for status in self.status_info.values():
            emoji = status['emoji']
            if emoji in task:
                task = task.replace(emoji, f":{self._get_slack_emoji_name(emoji)}:")
        
        return task

    def _get_slack_emoji_name(self, emoji: str) -> str:
        """Convert Unicode emoji to Slack emoji name."""
        # Mapping of Unicode emojis to Slack emoji names
        emoji_map = {
            "📝": "memo",
            "⚡": "zap",
            "🚧": "construction",
            "📅": "calendar",
            "➡️": "arrow_right",
            "✅": "white_check_mark",
            "🚫": "no_entry",
            # Add more mappings as needed
        }
        return emoji_map.get(emoji, "question")  # Default to :question: if not found 