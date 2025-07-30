from datetime import datetime
from typing import Tuple

def get_date_parts(date_obj: datetime) -> Tuple[str, str, str]:
    """Extract year, month, and day from datetime object."""
    return (date_obj.strftime("%Y"), date_obj.strftime("%m"), date_obj.strftime("%d"))

def parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD format.") 