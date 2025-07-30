from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import click
from rich.console import Console
import os

from .utils import get_date_parts, clean_section_header, split_into_sections, get_status_info
from . import config_manager
from .utils.text import split_into_sections
from .utils.file import read_file, write_file
from .utils.date import get_file_path

console = Console()

class TaskManager:
    """Manages task operations including creation, reading, and status updates."""
    
    def __init__(self, work_dir: Optional[Path] = None):
        self.config = config_manager.get_config()
        self.work_dir = work_dir or Path.cwd()
        self.status_info = get_status_info()

    def get_tasks_for_date(self, date: datetime) -> Dict[str, List[str]]:
        """Get all tasks for a specific date."""
        year, month, day = get_date_parts(date)
        daily_file = self.work_dir / year / month / day / self.config["daily_file_name"]
        
        if not daily_file.exists():
            return {}
            
        content = daily_file.read_text()
        sections = split_into_sections(content)
        tasks_by_project = {}
        
        for section in sections:
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            header = lines[0].strip()
            project_name = clean_section_header(header)
            tasks = [line.strip() for line in lines[1:] if line.strip().startswith('- [')]
            
            if tasks:
                tasks_by_project[project_name] = tasks
                
        return tasks_by_project

    def get_incomplete_tasks(self, date: datetime) -> Dict[str, List[str]]:
        """Get incomplete tasks for a specific date."""
        tasks_by_project = self.get_tasks_for_date(date)
        incomplete_tasks = {}
        
        completed_emojis = [info['emoji'] for info in self.status_info.values() 
                          if info.get('name', '').lower() in ['completed', 'cancelled']]
        
        for project, tasks in tasks_by_project.items():
            incomplete = [
                task for task in tasks 
                if not any(emoji in task for emoji in completed_emojis)
            ]
            if incomplete:
                incomplete_tasks[project] = incomplete
                
        return incomplete_tasks

    def carry_forward_tasks(self, from_date: datetime) -> Dict[str, List[str]]:
        """Get tasks to carry forward to next day."""
        incomplete_tasks = self.get_incomplete_tasks(from_date)
        carried_forward_emoji = next(
            (info['emoji'] for info in self.status_info.values() 
             if info.get('name', '').lower() == 'carried_forward'),
            "➡️"
        )
        
        carried_tasks = {}
        for project, tasks in incomplete_tasks.items():
            carried_tasks[project] = [
                f"{task} {carried_forward_emoji}" 
                for task in tasks
            ]
            
        return carried_tasks

    def create_daily_file(self, date: Optional[datetime] = None) -> str:
        """Create a new daily task file."""
        if date is None:
            date = datetime.now()
        
        file_path = get_file_path(date)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if not os.path.exists(file_path):
            # Use default template since we don't have config paths yet
            content = self._get_default_template()
            content = content.replace("{date}", date.strftime("%Y-%m-%d"))
            write_file(file_path, content)
            print(f"✅ Created daily file: {file_path}")
        else:
            print(f"⚠️ Daily file already exists: {file_path}")
        
        return file_path

    def complete_task(self, task_name: str, category: str, date: datetime) -> bool:
        """Mark a task as complete."""
        file_path = get_file_path(date)
        if not os.path.exists(file_path):
            return False
        
        content = read_file(file_path)
        lines = content.split('\n')
        found = False
        
        for i, line in enumerate(lines):
            if category in line and '##' in line:  # Found category section
                # Look for the task in the following lines until next section
                j = i + 1
                while j < len(lines) and not (lines[j].startswith('##')):
                    if task_name in lines[j] and '[ ]' in lines[j]:
                        lines[j] = lines[j].replace('[ ]', '[x]')
                        lines[j] = lines[j].replace('📝', '✅')
                        found = True
                        break
                    j += 1
                if found:
                    break
        
        if found:
            write_file(file_path, '\n'.join(lines))
            return True
        return False

    def _get_template(self) -> str:
        """Get the template content."""
        template_path = config_manager.get_template_path()
        try:
            return template_path.read_text()
        except Exception as e:
            console.print(f"❌ Error reading template: {e}", style="bold red")
            raise

    def _generate_daily_content(self, date: datetime, template: str, carried_tasks: Dict[str, List[str]]) -> str:
        """Generate content for daily file."""
        # Generate status legend
        status_legend = " | ".join([
            f"{info['emoji']} {info['name']}" for info in self.status_info.values()
        ])
        
        # Generate project sections
        project_sections = []
        for project in self.config["projects"]:
            project_name = project["name"]
            project_emoji = project["emoji"]
            
            # Get carried forward tasks or create new task template
            tasks = carried_tasks.get(project_name, [])
            if not tasks:
                planned_emoji = next(
                    (info['emoji'] for info in self.status_info.values() 
                     if info.get('name', '').lower() == 'planned'),
                    "📝"
                )
                tasks = [f"- [ ] New task {planned_emoji}"]
            
            project_sections.append(f"{project_emoji} {project_name}\n" + "\n".join(tasks))

        # Format template
        return template.format(
            date=date.strftime("%Y-%m-%d"),
            status_legend=status_legend,
            projects="\n\n".join(project_sections)
        )

    def _get_default_template(self) -> str:
        """Get default template content."""
        return """# Daily Tasks - {date}

## Status Legend
📝 Planned | ⚡ In Progress | 🚧 Blocked | 📅 Rescheduled | ➡️ Carried Forward | ✅ Completed | 🚫 Cancelled

## Tasks

🏠 Personal
- [ ] New task 📝

💼 Work
- [ ] New task 📝

📚 Learning
- [ ] New task 📝

## Notes
- 
"""

    def init_config(self):
        """Initialize configuration with default settings."""
        config_manager.init_default_config()

    def show_config_paths(self):
        """Show configuration paths."""
        config_manager.show_paths() 