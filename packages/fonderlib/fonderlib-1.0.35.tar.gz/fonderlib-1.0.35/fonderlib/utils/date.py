from datetime import datetime
from typing import Optional

def parse_datetime(date_str: Optional[str]) -> Optional[datetime]:
    """Convierte un string de fecha en un objeto datetime"""
    if not date_str:
        return None

    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None
