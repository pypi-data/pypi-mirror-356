from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import click
from rich.console import Console
import os
import re

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
        self.work_dir = Path(os.getcwd()) if work_dir is None else Path(work_dir)
        self.status_info = get_status_info()
        console.print(f"TaskManager initialized with work_dir: {self.work_dir}")

    def get_tasks_for_date(self, date: datetime) -> Dict[str, List[str]]:
        """Get all tasks for a specific date."""
        year, month, day = get_date_parts(date)
        file_name = self.config["daily_file_name"].format(year=year, month=month, day=day)
        file_path = self.work_dir / year / month / day / file_name
        
        console.print(f"Looking for file: {file_path}")
        
        if not os.path.exists(file_path):
            console.print(f"File not found: {file_path}")
            return {}
            
        content = read_file(str(file_path))
        tasks_by_project = {}
        
        # Split content into lines and process
        lines = content.split('\n')
        current_project = None
        current_tasks = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a project line
            project_found = False
            for project in self.config["projects"]:
                if line.startswith(project["emoji"]):
                    # Save previous project's tasks
                    if current_project and current_tasks:
                        tasks_by_project[current_project] = current_tasks
                        current_tasks = []
                    
                    current_project = f"{project['emoji']} {project['name']}"
                    console.print(f"Found project section: {current_project}")
                    project_found = True
                    break
                    
            if project_found:
                continue
                    
            # If we're in a project section and this is a task, collect it
            if current_project and line.startswith('- ['):
                current_tasks.append(line)
                console.print(f"Added task to {current_project}: {line}")
        
        # Don't forget to save the last project's tasks
        if current_project and current_tasks:
            tasks_by_project[current_project] = current_tasks
                
        console.print(f"Found tasks: {tasks_by_project}")
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

    def create_daily_file(self, date: Optional[datetime] = None, template_only: bool = False) -> str:
        """Create a new daily task file."""
        if date is None:
            date = datetime.now()
        
        year, month, day = get_date_parts(date)
        file_name = self.config["daily_file_name"].format(year=year, month=month, day=day)
        file_path = self.work_dir / year / month / day / file_name
        
        if not os.path.exists(file_path):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(str(file_path)), exist_ok=True)
            
            # Get template and tasks
            template = self._get_template()
            
            use_last_date = False
            last_date = None
            
            if not template_only:
                # First check yesterday's date
                yesterday = date - timedelta(days=1)
                yesterday_file = self.work_dir / get_date_parts(yesterday)[0] / get_date_parts(yesterday)[1] / get_date_parts(yesterday)[2] / self.config["daily_file_name"].format(year=get_date_parts(yesterday)[0], month=get_date_parts(yesterday)[1], day=get_date_parts(yesterday)[2])
                
                # Then find the most recent available date
                last_date = self.find_last_available_date(date)
                
                if os.path.exists(yesterday_file):
                    # If yesterday's file exists, ask about using it
                    console.print(f"\nCreating file for: {date.strftime(self.config['date_format'])}", style="blue")
                    use_last_date = click.confirm(f"Do you want to carry forward tasks from yesterday ({yesterday.strftime(self.config['date_format'])})?", default=True)
                    if use_last_date:
                        last_date = yesterday
                elif last_date:
                    # If yesterday's file doesn't exist but we found an earlier date
                    console.print(f"\nCreating file for: {date.strftime(self.config['date_format'])}", style="blue")
                    console.print(f"Yesterday's file ({yesterday.strftime(self.config['date_format'])}) not found.", style="yellow")
                    console.print(f"Found last available date: {last_date.strftime(self.config['date_format'])}", style="blue")
                    use_last_date = click.confirm(f"Do you want to use tasks from {last_date.strftime(self.config['date_format'])}?", default=True)
                    if not use_last_date:
                        last_date = None
            
            # Generate content
            content = self._generate_daily_content(date, template, last_date if use_last_date else None)
            write_file(str(file_path), content)
            console.print(f"✅ Created daily file: {file_path}", style="green")
        else:
            console.print(f"⚠️ Daily file already exists: {file_path}", style="yellow")
        
        return str(file_path)

    def complete_task(self, task_name: str, category: str, date: datetime) -> bool:
        """Mark a task as complete."""
        year, month, day = get_date_parts(date)
        file_name = self.config["daily_file_name"].format(year=year, month=month, day=day)
        file_path = self.work_dir / year / month / day / file_name
        
        if not os.path.exists(file_path):
            return False
        
        content = read_file(str(file_path))
        lines = content.split('\n')
        found = False
        
        for i, line in enumerate(lines):
            if category in line and not line.startswith('##'):  # Found category section
                # Look for the task in the following lines until next section
                j = i + 1
                while j < len(lines) and not any(p["emoji"] in lines[j] for p in self.config["projects"]):
                    if task_name in lines[j] and '[ ]' in lines[j]:
                        lines[j] = lines[j].replace('[ ]', '[x]')
                        lines[j] = lines[j].replace('📝', '✅')
                        found = True
                        break
                    j += 1
                if found:
                    break
        
        if found:
            write_file(str(file_path), '\n'.join(lines))
            return True
        return False

    def find_last_available_date(self, current_date: datetime) -> Optional[datetime]:
        """Find the most recent date before current_date that has a daily file."""
        try:
            check_date = current_date - timedelta(days=1)
            for _ in range(30):
                year, month, day = get_date_parts(check_date)
                file_name = self.config["daily_file_name"].format(year=year, month=month, day=day)
                check_file = self.work_dir / year / month / day / file_name
                if os.path.exists(check_file):
                    return check_date
                check_date -= timedelta(days=1)
            return None
        except Exception as e:
            console.print(f"⚠️ Error finding last available date: {e}", style="yellow")
            return None

    def _get_template(self) -> str:
        """Get the template content."""
        template_path = config_manager.get_template_path()
        try:
            return template_path.read_text()
        except Exception as e:
            console.print(f"❌ Error reading template: {e}", style="bold red")
            raise

    def _generate_daily_content(self, date: datetime, template: str, last_date: Optional[datetime] = None) -> str:
        """Generate content for daily file."""
        # Get status legend from config
        status_info = get_status_info()
        status_legend = " | ".join([
            f"{info['emoji']} {info['name']}" for info in status_info.values()
        ])
        
        # Get tasks from previous date if available
        tasks_by_project = {}
        if last_date:
            tasks_by_project = self.get_incomplete_tasks(last_date)
            
        # Get planned emoji from config
        planned_emoji = next(
            (info['emoji'] for info in status_info.values() 
             if info.get('name', '').lower() == 'planned'),
            "📝"  # Fallback emoji
        )
        
        # Generate project sections
        project_sections = []
        for project in self.config["projects"]:
            project_name = project["name"]
            project_emoji = project["emoji"]
            
            tasks = []
            if last_date and f"{project_emoji} {project_name}" in tasks_by_project:
                tasks.extend(tasks_by_project[f"{project_emoji} {project_name}"])
            
            # Always add a new task template
            tasks.append(f"- [ ] New task {planned_emoji}")
            
            # Add project section without ## prefix
            project_section = f"{project_emoji} {project_name}\n"
            project_section += "\n".join(tasks)
            project_sections.append(project_section)
            
        # Replace template variables
        template_data = {
            'date': date.strftime("%Y-%m-%d"),
            'status_legend': status_legend,
            'projects': '\n\n'.join(project_sections)
        }
        
        return template.format(**template_data)

    def _get_default_template(self) -> str:
        """Get default template content."""
        return """# Daily Tasks - {date}

## Status Legend
{status_legend}

{projects}

## Notes
- 
"""

    def init_config(self):
        """Initialize configuration with default settings."""
        config_manager.init_default_config()

    def show_config_paths(self):
        """Show configuration paths."""
        config_manager.show_paths()

    def get_project_tasks(self, project_name: str, emoji: str, date_obj: datetime, last_available_date: Optional[datetime] = None) -> str:
        """Get tasks for a project, including carried forward tasks."""
        try:
            prev_date = last_available_date if last_available_date else (date_obj - timedelta(days=1))
            year, month, day = get_date_parts(prev_date)
            file_name = self.config["daily_file_name"].format(year=year, month=month, day=day)
            prev_file = self.work_dir / year / month / day / file_name
            
            tasks = []
            status_info = get_status_info()
            
            # Get status emojis from config
            completed_emojis = [info['emoji'] for info in status_info.values() 
                              if info.get('name', '').lower() in ['completed', 'cancelled']]
            planned_emoji = next(
                (info['emoji'] for info in status_info.values() 
                 if info.get('name', '').lower() == 'planned'),
                "📝"
            )
            
            if os.path.exists(prev_file):
                content = read_file(str(prev_file))
                lines = content.split('\n')
                in_project = False
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                        
                    # Check if this is our project section
                    if line.startswith(f"{emoji}"):
                        in_project = True
                        continue
                    
                    # Check if we're entering a new project section
                    if any(p["emoji"] in line for p in self.config["projects"]):
                        in_project = False
                        continue
                    
                    # If we're in our project section and this is a task
                    if in_project and line.startswith('- ['):
                        # Only transfer non-completed tasks
                        if not any(emoji in line for emoji in completed_emojis):
                            # Skip template tasks
                            if not line.strip().endswith(f"New task {planned_emoji}"):
                                tasks.append(line.strip())
            
            # Always add a new task template with planned emoji from config
            tasks.append(f"- [ ] New task {planned_emoji}")
            return '\n'.join(tasks)
            
        except Exception as e:
            console.print(f"⚠️ Error getting tasks for {project_name}: {e}", style="yellow")
            return f"- [ ] New task {planned_emoji}" 