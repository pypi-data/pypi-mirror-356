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

    def create_daily_file(self, date: Optional[datetime] = None, template_only: bool = False) -> str:
        """Create a new daily task file."""
        if date is None:
            date = datetime.now()
        
        file_path = get_file_path(date)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if not os.path.exists(file_path):
            # Get template and tasks
            template = self._get_template()
            
            use_last_date = False
            last_date = None
            
            if not template_only:
                # First check yesterday's date
                yesterday = date - timedelta(days=1)
                yesterday_file = get_file_path(yesterday)
                
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
                else:
                    console.print("\n⚠️ No previous daily files found in the last 30 days.", style="yellow")
                    use_last_date = False
            
            # Generate content
            content = self._generate_daily_content(date, template, last_date if use_last_date else None)
            write_file(file_path, content)
            console.print(f"✅ Created daily file: {file_path}", style="green")
        else:
            console.print(f"⚠️ Daily file already exists: {file_path}", style="yellow")
        
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

    def find_last_available_date(self, current_date: datetime) -> Optional[datetime]:
        """Find the most recent date before current_date that has a daily file."""
        try:
            check_date = current_date - timedelta(days=1)
            for _ in range(30):
                check_file = get_file_path(check_date)
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
        
        # Generate project sections
        project_sections = []
        template_data = {'date': date.strftime("%Y-%m-%d")}
        
        for project in self.config["projects"]:
            project_name = project["name"]
            project_emoji = project["emoji"]
            tasks = self.get_project_tasks(project_name, project_emoji, date, last_date)
            project_sections.append(f"{project_emoji} {project_name}\n{tasks}")

        template_data['projects'] = '\n\n'.join(project_sections)
        template_data['status_legend'] = status_legend
        
        return template.format(**template_data)

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

    def get_project_tasks(self, project_name: str, emoji: str, date_obj: datetime, last_available_date: Optional[datetime] = None) -> str:
        """Get tasks for a project, including carried forward tasks."""
        try:
            prev_date = last_available_date if last_available_date else (date_obj - timedelta(days=1))
            prev_file = get_file_path(prev_date)
            
            tasks = []
            status_info = get_status_info()
            
            # Get status emojis from config
            completed_emojis = [info['emoji'] for info in status_info.values() 
                              if info.get('name', '').lower() in ['completed', 'cancelled']]
            carried_forward_emoji = next(
                (info['emoji'] for info in status_info.values() 
                 if info.get('name', '').lower() == 'carried_forward'),
                "➡️"
            )
            planned_emoji = next(
                (info['emoji'] for info in status_info.values() 
                 if info.get('name', '').lower() == 'planned'),
                "📝"
            )
            
            if os.path.exists(prev_file):
                content = read_file(prev_file)
                sections = split_into_sections(content)
                
                # Find the project section
                for section in sections:
                    section_lines = section.strip().split('\n')
                    if not section_lines:
                        continue
                    
                    header = clean_section_header(section_lines[0])
                    if header == f"{emoji} {project_name}":
                        for line in section_lines[1:]:  # Skip header
                            if line.strip().startswith('- ['):
                                # Check if task is not completed using dynamic emojis
                                if not any(emoji in line for emoji in completed_emojis):
                                    if not any(template in line for template in self.config["template_content"]["tasks"]):
                                        # Add carried forward emoji to tasks from previous dates
                                        if last_available_date and (date_obj - last_available_date).days > 1:
                                            tasks.append(f"{line.strip()} {carried_forward_emoji}")
                                        else:
                                            tasks.append(line.strip())
                        break
            
            # Always add a new task template with planned emoji from config
            tasks.append(f"- [ ] New task {planned_emoji}")
            return '\n'.join(tasks)
            
        except Exception as e:
            console.print(f"⚠️ Error getting tasks for {project_name}: {e}", style="yellow")
            return f"- [ ] New task {planned_emoji}" 