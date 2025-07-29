def set_obj_value_or_default(obj, key):
    return None if obj.get(f"{key}") is False else obj[key]
