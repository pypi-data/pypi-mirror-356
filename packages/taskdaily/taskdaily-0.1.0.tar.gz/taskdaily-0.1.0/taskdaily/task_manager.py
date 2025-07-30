from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import click
from rich.console import Console

from .utils import get_date_parts, clean_section_header, split_into_sections, get_status_info
from . import config_manager

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

    def create_daily_file(self, date: datetime, template_only: bool = False) -> None:
        """Create a new daily file."""
        year, month, day = get_date_parts(date)
        day_path = self.work_dir / year / month / day
        day_path.mkdir(parents=True, exist_ok=True)

        daily_file = day_path / self.config["daily_file_name"]
        if daily_file.exists():
            return

        template = self._get_template()
        prev_date = date - timedelta(days=1)
        
        # Check for tasks to carry forward
        carried_tasks = {}
        if not template_only:
            carried_tasks = self.carry_forward_tasks(prev_date)

        # Generate content
        content = self._generate_daily_content(date, template, carried_tasks)
        daily_file.write_text(content)
        console.print(f"✅ Created daily file: {daily_file}", style="green")

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