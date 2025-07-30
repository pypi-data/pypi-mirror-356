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
        sections = []
        
        # Add header with divider
        header = f"{'=' * 30}\n"
        header += f"{'EOD REPORT' if is_report else 'DAILY PLAN'} - {date_str}\n"
        header += f"{'=' * 30}"
        sections.append(header)

        # Get planned emoji from config
        planned_emoji = next(
            (info['emoji'] for info in self.status_info.values() 
             if info.get('name', '').lower() == 'planned'),
            "📝"  # Fallback emoji
        )

        # Process each project
        for project_name, project_tasks in tasks.items():
            if not project_tasks:
                continue

            filtered_tasks = []
            for task in project_tasks:
                # Skip template tasks
                if task.strip().endswith(f"New task {planned_emoji}"):
                    continue
                    
                # For reports, exclude planned tasks
                if is_report and planned_emoji in task:
                    continue
                    
                # For daily plan, remove planned emoji
                if not is_report:
                    task = task.replace(planned_emoji, "").strip()
                    # Clean up any double spaces from emoji removal
                    while "  " in task:
                        task = task.replace("  ", " ")
                
                filtered_tasks.append(task)

            if filtered_tasks:
                # Add project header (without bold formatting)
                sections.append(f"\n{project_name}")
                
                # Add tasks with proper indentation
                for task in filtered_tasks:
                    task_text = self._convert_to_slack_format(task)
                    sections.append(f"  {task_text}")
                
                # Add divider after each project
                sections.append(f"{'-' * 45}")

        return "\n".join(sections)

    def _convert_to_slack_format(self, task: str) -> str:
        """Convert markdown task format to Slack format."""
        # Remove markdown checkbox and add better bullet points
        task = task.replace("- [ ]", "○").replace("- [x]", "●")
        
        # Convert status emojis
        for status in self.status_info.values():
            emoji = status['emoji']
            if emoji in task:
                task = task.replace(emoji, f":{self._get_slack_emoji_name(emoji)}:")
        
        return task

    def _init_emoji_map(self) -> None:
        """Initialize emoji mapping."""
        # Base emoji map for future use if needed
        self._emoji_map = {
            "📝": "memo",
            "⚡": "zap",
            "🚧": "construction",
            "📅": "calendar",
            "➡️": "arrow_right",
            "✅": "white_check_mark",
            "🚫": "no_entry",
            "🏠": "house",
            "💼": "briefcase",
            "📚": "books",
        }
        
        # Add any custom emojis from config
        for status in self.status_info.values():
            emoji = status['emoji']
            if emoji not in self._emoji_map:
                name = status['name'].lower().replace(" ", "_")
                self._emoji_map[emoji] = name

    def _get_slack_emoji_name(self, emoji: str) -> str:
        """Convert Unicode emoji to Slack emoji name."""
        return self._emoji_map.get(emoji, "question")  # Default to :question: if not found 