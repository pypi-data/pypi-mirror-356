import json
import datetime
from typing import Dict, List, Union


class DateTimeJSONEncoder(json.JSONEncoder):
    """Encoder JSON personalizado que maneja objetos datetime"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


def serialize_datetime_json(data: Union[Dict, List]) -> Union[Dict, List]:
    """
    Convierte cualquier objeto datetime en una estructura de datos a string ISO
    para hacerlo serializable a JSON

    Args:
        data: Diccionario o lista que puede contener objetos datetime

    Returns:
        La misma estructura con los datetime convertidos a strings
    """
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if isinstance(value, datetime.datetime):
                result[key] = value.isoformat()
            elif isinstance(value, (dict, list)):
                result[key] = serialize_datetime_json(value)
            else:
                result[key] = value
        return result
    elif isinstance(data, list):
        return [
            serialize_datetime_json(item) if isinstance(item, (dict, list))
            else (item.isoformat() if isinstance(item, datetime.datetime) else item)
            for item in data
        ]
    return data