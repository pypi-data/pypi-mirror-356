from datetime import datetime
from typing import Tuple, List, Dict, Any
import re
from . import config_manager

def get_date_parts(date_obj: datetime) -> Tuple[str, str, str]:
    """Extract year, month, and day from datetime object."""
    return (date_obj.strftime("%Y"), date_obj.strftime("%m"), date_obj.strftime("%d"))

def standardize_section_header(line: str) -> str:
    """Standardize section header by removing leading/trailing spaces and special characters."""
    return re.sub(r'[^\w\s]', '', line.strip()).lower()

def clean_section_header(header: str) -> str:
    """Clean section header for comparison."""
    return ' '.join(header.strip().split())

def get_config() -> Dict[str, Any]:
    """Get configuration with user preferences."""
    return config_manager.get_config()

def get_section_markers() -> List[str]:
    """Get all section markers (emojis and special characters) from config."""
    config = get_config()
    markers = ['#']  # Always include # as a section marker
    
    # Add project emojis
    for project in config.get('projects', []):
        if 'emoji' in project:
            markers.append(project['emoji'])
    
    # Add status emojis
    for status in config.get('status', {}).values():
        if 'emoji' in status:
            markers.append(status['emoji'])
    
    return markers

def get_status_info() -> Dict[str, Dict[str, str]]:
    """Get status information from config."""
    config = get_config()
    return config.get('status', {})

def split_into_sections(content: str) -> List[str]:
    """Split content into sections based on headers."""
    sections = []
    current_section = []
    markers = get_section_markers()
    
    for line in content.split('\n'):
        if line.strip() and any(line.startswith(m) for m in markers):
            if current_section:
                sections.append('\n'.join(current_section))
            current_section = [line]
        else:
            current_section.append(line)
    
    if current_section:
        sections.append('\n'.join(current_section))
    
    return sections

def parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD format.") 