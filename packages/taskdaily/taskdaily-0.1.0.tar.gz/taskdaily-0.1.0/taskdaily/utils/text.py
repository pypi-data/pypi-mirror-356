import re
from typing import List, Dict, Any
from .. import config_manager

def standardize_section_header(line: str) -> str:
    """Standardize section header by removing leading/trailing spaces and special characters."""
    return re.sub(r'[^\w\s]', '', line.strip()).lower()

def clean_section_header(header: str) -> str:
    """Clean section header for comparison."""
    return ' '.join(header.strip().split())

def split_into_sections(content: str, markers: List[str]) -> List[str]:
    """Split content into sections based on headers."""
    sections = []
    current_section = []
    
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

def get_status_info() -> Dict[str, Any]:
    """Get status information from config."""
    config = config_manager.get_config()
    return config.get("status", {
        "planned": {"name": "Planned", "emoji": "📝"},
        "in_progress": {"name": "In Progress", "emoji": "⚡"},
        "blocked": {"name": "Blocked", "emoji": "🚧"},
        "rescheduled": {"name": "Rescheduled", "emoji": "📅"},
        "carried_forward": {"name": "Carried Forward", "emoji": "➡️"},
        "completed": {"name": "Completed", "emoji": "✅"},
        "cancelled": {"name": "Cancelled", "emoji": "🚫"}
    }) 