from typing import Union
from enum import Enum, StrEnum


def num_validator(value: int, min_value: int, max_value: int):
    if min_value <= value <= max_value:
        return value
    else:
        if value < min_value:
            return min_value
        else:
            return max_value


def enum_value_validator(value: str, enum_class: type[Union[Enum, StrEnum]]) -> bool:
    return any(value.lower() == member.value for member in enum_class)
