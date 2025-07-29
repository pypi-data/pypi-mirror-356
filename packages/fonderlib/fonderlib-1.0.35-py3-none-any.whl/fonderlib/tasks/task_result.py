from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TaskResult:
    """Task result"""

    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[Exception] = None
    elapsed_time: float = 0
    processed_count: int = 0
