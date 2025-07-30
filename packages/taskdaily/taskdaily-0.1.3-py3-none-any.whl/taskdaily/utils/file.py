from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta

def ensure_directory_exists(path: Path) -> None:
    """Ensure directory exists, create if it doesn't."""
    path.mkdir(parents=True, exist_ok=True)

def find_last_available_file(base_path: Path, current_date: datetime, file_name: str, max_days: int = 30) -> Optional[Path]:
    """Find the most recent file before current_date."""
    check_date = current_date - timedelta(days=1)
    for _ in range(max_days):
        check_file = base_path / check_date.strftime("%Y") / check_date.strftime("%m") / check_date.strftime("%d") / file_name
        if check_file.exists():
            return check_file
        check_date -= timedelta(days=1)
    return None

def read_file_content(file_path: Path) -> str:
    """Read file content safely."""
    try:
        return file_path.read_text()
    except Exception as e:
        raise IOError(f"Failed to read file {file_path}: {e}")

def write_file_content(file_path: Path, content: str) -> None:
    """Write content to file safely."""
    try:
        file_path.write_text(content)
    except Exception as e:
        raise IOError(f"Failed to write to file {file_path}: {e}")

def read_file(file_path: str) -> str:
    """Read content from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file_path: str, content: str) -> None:
    """Write content to a file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content) 