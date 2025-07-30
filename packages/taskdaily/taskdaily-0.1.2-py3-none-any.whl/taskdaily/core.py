import os
import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
from typing import Tuple, Dict, Any, Optional
import yaml
from rich.console import Console
from rich.table import Table
import shutil
import tarfile
import time
import click

from .utils import get_date_parts, clean_section_header, split_into_sections, get_status_info
from . import config_manager

console = Console()

class DailyManagerError(Exception):
    """Base exception class for Daily Manager errors."""
    pass

class ConfigError(DailyManagerError):
    """Configuration related errors."""
    pass

class BackupError(DailyManagerError):
    """Backup related errors."""
    pass

class DailyManager:
    def __init__(self):
        self.config = config_manager.get_config()
        self.setup_logging()
        self.base_path = Path(__file__).resolve().parent
        self.repo_path = Path.cwd()  # Use current directory as repo path

    def setup_logging(self):
        """Configure logging based on settings."""
        logging.basicConfig(
            level=getattr(logging, self.config['logging']['level']),
            format=self.config['logging']['format']
        )

    def create_backup(self) -> None:
        """Create a backup of the daily notes."""
        if not self.config.get('backup', {}).get('enabled', False):
            return

        try:
            backup_dir = self.repo_path / self.config['backup']['directory']
            backup_dir.mkdir(exist_ok=True)

            # Clean old backups
            retention_days = self.config['backup']['retention_days']
            current_time = time.time()
            for backup_file in backup_dir.glob('*.tar.gz'):
                if (current_time - backup_file.stat().st_mtime) > (retention_days * 86400):
                    backup_file.unlink()

            # Create new backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"daily_notes_backup_{timestamp}"
            
            if self.config['backup']['compress']:
                backup_path = backup_dir / f"{backup_name}.tar.gz"
                with tarfile.open(backup_path, "w:gz") as tar:
                    for year_dir in self.repo_path.glob('[0-9][0-9][0-9][0-9]'):
                        if year_dir.is_dir():
                            tar.add(year_dir, arcname=year_dir.name)
            else:
                backup_path = backup_dir / backup_name
                for year_dir in self.repo_path.glob('[0-9][0-9][0-9][0-9]'):
                    if year_dir.is_dir():
                        shutil.copytree(year_dir, backup_path / year_dir.name)

            console.print(f"✅ Created backup: {backup_path}", style="green")

        except Exception as e:
            raise BackupError(f"Failed to create backup: {e}")

    def should_create_backup(self) -> bool:
        """Determine if backup should be created based on frequency setting."""
        if not self.config.get('backup', {}).get('enabled', False):
            return False

        backup_dir = self.repo_path / self.config['backup']['directory']
        if not backup_dir.exists():
            return True

        frequency = self.config['backup']['frequency']
        latest_backup = None
        
        for backup in backup_dir.glob('*.tar.gz'):
            if not latest_backup or backup.stat().st_mtime > latest_backup.stat().st_mtime:
                latest_backup = backup

        if not latest_backup:
            return True

        last_backup_time = datetime.fromtimestamp(latest_backup.stat().st_mtime)
        now = datetime.now()

        if frequency == 'daily':
            return last_backup_time.date() < now.date()
        elif frequency == 'weekly':
            return (now - last_backup_time).days >= 7
        elif frequency == 'monthly':
            return (now.year, now.month) != (last_backup_time.year, last_backup_time.month)
        
        return False

    def get_template(self) -> str:
        """Read the template from user config or default."""
        template_path = config_manager.get_template_path()
        try:
            if template_path.exists():
                return template_path.read_text()
            else:
                console.print(f"❌ Template file not found: {template_path}", style="bold red")
                sys.exit(1)
        except OSError as e:
            console.print(f"❌ Error reading template file: {e}", style="bold red")
            sys.exit(1)

    def find_last_available_date(self, current_date: datetime) -> Optional[datetime]:
        """Find the most recent date before current_date that has a daily file."""
        try:
            check_date = current_date - timedelta(days=1)
            for _ in range(30):
                year, month, day = get_date_parts(check_date)
                check_file = self.repo_path / year / month / day / self.config["daily_file_name"]
                if check_file.exists():
                    return check_date
                check_date -= timedelta(days=1)
            return None
        except Exception as e:
            console.print(f"⚠️ Error finding last available date: {e}", style="yellow")
            return None

    def get_project_tasks(self, project_name: str, emoji: str, date_obj: datetime, last_available_date: Optional[datetime] = None) -> str:
        """Get tasks for a project, including carried forward tasks."""
        try:
            prev_date = last_available_date if last_available_date else (date_obj - timedelta(days=1))
            year, month, day = get_date_parts(prev_date)
            prev_file = self.repo_path / year / month / day / self.config["daily_file_name"]
            
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
            
            if prev_file.exists():
                content = prev_file.read_text()
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
            # Use planned emoji from config even in error case
            return f"- [ ] New task {planned_emoji}"

    def create_day_file(self, date_obj: datetime, template_only: bool = False) -> None:
        """Create daily log file and update monthly README."""
        try:
            year, month, day = get_date_parts(date_obj)
            day_path = self.repo_path / year / month / day
            month_path = self.repo_path / year / month
            day_path.mkdir(parents=True, exist_ok=True)

            daily_file = day_path / self.config["daily_file_name"]
            if not daily_file.exists():
                template = self.get_template()
                
                use_last_date = False
                last_date = None
                
                if not template_only:
                    # First check yesterday's date
                    yesterday = date_obj - timedelta(days=1)
                    yesterday_file = self.repo_path / yesterday.strftime("%Y") / yesterday.strftime("%m") / yesterday.strftime("%d") / self.config["daily_file_name"]
                    
                    # Then find the most recent available date
                    last_date = self.find_last_available_date(date_obj)
                    
                    if yesterday_file.exists():
                        # If yesterday's file exists, ask about using it
                        console.print(f"\nCreating file for: {date_obj.strftime(self.config['date_format'])}", style="blue")
                        use_last_date = click.confirm(f"Do you want to carry forward tasks from yesterday ({yesterday.strftime(self.config['date_format'])})?", default=True)
                        if use_last_date:
                            last_date = yesterday
                    elif last_date:
                        # If yesterday's file doesn't exist but we found an earlier date
                        console.print(f"\nCreating file for: {date_obj.strftime(self.config['date_format'])}", style="blue")
                        console.print(f"Yesterday's file ({yesterday.strftime(self.config['date_format'])}) not found.", style="yellow")
                        console.print(f"Found last available date: {last_date.strftime(self.config['date_format'])}", style="blue")
                        use_last_date = click.confirm(f"Do you want to use tasks from {last_date.strftime(self.config['date_format'])}?", default=True)
                    else:
                        console.print("\n⚠️ No previous daily files found in the last 30 days.", style="yellow")
                        use_last_date = False
                
                # Get status legend from config
                status_info = get_status_info()
                status_legend = " | ".join([
                    f"{info['emoji']} {info['name']}" for info in status_info.values()
                ])
                
                project_sections = []
                template_data = {'date': date_obj.strftime("%Y-%m-%d")}
                
                for project in self.config["projects"]:
                    project_name = project["name"]
                    project_emoji = project["emoji"]
                    tasks = self.get_project_tasks(project_name, project_emoji, date_obj, last_date if use_last_date else None)
                    project_sections.append(f"{project_emoji} {project_name}\n{tasks}")

                template_data['projects'] = '\n\n'.join(project_sections)
                template_data['status_legend'] = status_legend
                
                content = template.format(**template_data)
                daily_file.write_text(content)
                console.print(f"✅ Created daily file: {daily_file}", style="green")

        except Exception as e:
            console.print(f"❌ Error creating daily file: {e}", style="bold red")
            sys.exit(1)

    def git_push(self, commit_date: str) -> None:
        """Push changes to git repository."""
        try:
            if not self.config.get('git', {}).get('enabled', False):
                return

            commands = [
                ['git', 'add', '.'],
                ['git', 'commit', '-m', f"Update daily notes for {commit_date}"],
                ['git', 'push']
            ]

            for cmd in commands:
                result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)
                if result.returncode != 0 and not (cmd[1] == 'commit' and 'nothing to commit' in result.stderr):
                    console.print(f"❌ Git command failed: {' '.join(cmd)}", style="bold red")
                    console.print(f"Error: {result.stderr}", style="red")
                    return

            console.print("✅ Changes pushed to git repository", style="green")

        except Exception as e:
            console.print(f"❌ Git operation failed: {e}", style="bold red") 