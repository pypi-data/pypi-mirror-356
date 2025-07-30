from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

class OutputHandler(ABC):
    """Base class for all output handlers."""
    
    @abstractmethod
    def send(self, content: str, **kwargs) -> bool:
        """Send content through the handler."""
        pass

    @abstractmethod
    def format_content(self, tasks: Dict[str, Any], date: datetime, is_report: bool = False) -> str:
        """Format content for the specific handler."""
        pass 