from pathlib import Path

# Default configuration paths
DEFAULT_CONFIG_DIR = Path(__file__).resolve().parent.parent / "templates"
USER_CONFIG_DIR = Path.home() / ".config" / "daily-task"
USER_CONFIG_FILE = USER_CONFIG_DIR / "config.yaml"
USER_TEMPLATE_FILE = USER_CONFIG_DIR / "daily_template.md"

# Default status configuration
DEFAULT_STATUS = {
    "planned": {"name": "Planned", "emoji": "📝"},
    "in_progress": {"name": "In Progress", "emoji": "⚡"},
    "blocked": {"name": "Blocked", "emoji": "🚧"},
    "rescheduled": {"name": "Rescheduled", "emoji": "📅"},
    "carried_forward": {"name": "Carried Forward", "emoji": "➡️"},
    "completed": {"name": "Completed", "emoji": "✅"},
    "cancelled": {"name": "Cancelled", "emoji": "🚫"}
}

# Default project configuration
DEFAULT_PROJECTS = [
    {"name": "Personal", "emoji": "🏠"},
    {"name": "Work", "emoji": "💼"},
    {"name": "Learning", "emoji": "📚"}
]

# Default logging configuration
DEFAULT_LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# Default backup configuration
DEFAULT_BACKUP = {
    "enabled": True,
    "directory": "backups",
    "frequency": "daily",
    "retention_days": 30,
    "compress": True
} 