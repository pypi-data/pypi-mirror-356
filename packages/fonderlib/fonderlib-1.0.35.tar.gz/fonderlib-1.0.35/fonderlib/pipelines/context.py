from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Context:
    """Context class"""

    limit: Optional[int] = None
    days: Optional[int] = None
    page: Optional[int] = None
