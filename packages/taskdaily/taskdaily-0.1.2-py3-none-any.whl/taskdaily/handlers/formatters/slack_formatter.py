from datetime import datetime
from typing import Dict, Any, List

class SlackFormatter:
    """Formats tasks for Slack messages."""
    
    def __init__(self, status_info: Dict[str, Dict[str, str]]):
        self.status_info = status_info
        self._init_emoji_map()

    def format_message(self, tasks: Dict[str, List[str]], date: datetime, is_report: bool = False) -> str:
        """Format tasks into a Slack message."""
        date_str = date.strftime("%Y-%m-%d")
        header = f"*EOD Report {date_str}*" if is_report else f"*Daily Plan {date_str}*"
        sections = []

        # Get planned emoji for filtering
        planned_emoji = "📝"  # Default
        for status in self.status_info.values():
            if status.get('name', '').lower() == 'planned':
                planned_emoji = status['emoji']
                break

        for project_name, project_tasks in tasks.items():
            if not project_tasks:
                continue

            filtered_tasks = []
            for task in project_tasks:
                # For reports, exclude planned tasks and template tasks
                if is_report and planned_emoji in task:
                    continue
                if any(template in task for template in ["New task 📝", "New task 📋"]):
                    continue
                filtered_tasks.append(task)

            if filtered_tasks:
                sections.append(f"\n*{project_name}*")
                for task in filtered_tasks:
                    task_text = self._convert_to_slack_format(task)
                    sections.append(task_text)

        return header + "\n" + "\n".join(sections)

    def _convert_to_slack_format(self, task: str) -> str:
        """Convert markdown task format to Slack format."""
        # Remove markdown checkbox
        task = task.replace("- [ ]", "•").replace("- [x]", "✓")
        
        # Convert status emojis
        for status in self.status_info.values():
            emoji = status['emoji']
            if emoji in task:
                task = task.replace(emoji, f":{self._emoji_map.get(emoji, 'question')}:")
        
        return task

    def _init_emoji_map(self) -> None:
        """Initialize emoji mapping."""
        self._emoji_map = {
            "📝": "memo",
            "⚡": "zap",
            "🚧": "construction",
            "📅": "calendar",
            "➡️": "arrow_right",
            "✅": "white_check_mark",
            "🚫": "no_entry",
        } 