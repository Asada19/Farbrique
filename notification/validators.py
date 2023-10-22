import re
from typing import Dict, Union
from rest_framework.exceptions import ValidationError


def phone_number_validator(phone_number: str) -> bool:

    if not re.match(r'^7\d{10}$', phone_number):
        raise ValidationError("Invalid phone number")
    return True


def filter_validator(filter_parameters: Dict[str, Union[str, list]]) -> bool:
    if not isinstance(filter_parameters, dict):
        raise ValidationError("Filter parameters must be a dictionary")

    allowed_keys = {'operator_code', 'tag'}
    for key, value in filter_parameters.items():
        if key not in allowed_keys:
            raise ValidationError(f"Invalid filter parameter: {key}")
        if not isinstance(value, list):
            raise ValidationError(f"Filter parameter '{key}' must be a list")
        if not all(isinstance(item, str) for item in value):
            raise ValidationError(f"Filter parameter '{key}' must contain only strings")

    if len(filter_parameters) > 2:
        raise ValidationError("Filter can contain only 'tag' and 'operator_code'")

    return True
