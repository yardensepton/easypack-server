from typing import Any

from src.exceptions.input_error import InputError


def validate_non_none_fields(obj: Any) -> bool:
    fields_to_check = {key: value for key, value in obj.dict().items() if key != 'id'}

    missing_fields = [field_name for field_name, field_value in fields_to_check.items()
                      if field_value is None or not field_value.strip()]
    if missing_fields:
        missing_fields_str = ', '.join(missing_fields)
        raise InputError(f"Fields cannot be empty: {missing_fields_str}")
    return True
