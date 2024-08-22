from src.exceptions.input_error import InputError
from src.repositories import T


def validate_non_none_fields(obj: T) -> bool:
    # Create a dictionary of fields to check, excluding fields that are dicts and the 'id' field
    fields_to_check = {
        key: value for key, value in obj.__dict__.items()
        if key != 'id' and not isinstance(value, dict)
    }

    # Find fields that are None or empty (for strings)
    missing_fields = [
        field_name for field_name, field_value in fields_to_check.items()
        if field_value is None or (isinstance(field_value, str) and not field_value.strip())
    ]

    # Raise an error if any required fields are missing
    if missing_fields:
        missing_fields_str = ', '.join(missing_fields)
        raise InputError(f"Fields cannot be empty: {missing_fields_str}")

    return True
