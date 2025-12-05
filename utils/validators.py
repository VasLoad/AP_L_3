from typing import Union
from enum import Enum, StrEnum


def num_validator(value: int, min_value: int, max_value: int):
    """
    Валидатор целых чисел.

    Args:
        value: Целое число для валидации
        min_value: Минимальное значение
        max_value: Максимальное значение

    Returns:
        Целое число после валидации.
    """

    if min_value <= value <= max_value:
        return value
    else:
        if value < min_value:
            return min_value
        else:
            return max_value


def enum_value_validator(value: str, enum_class: type[Union[Enum, StrEnum]]) -> bool:
    """
    Валидатор типов данных Enum и StrEnum.

    Args:
        value: Значение для валидации
        enum_class: Класс Enum или StrEnum

    Returns:
        Соответствует ли значение классу
    """

    return any(value.lower() == member.value for member in enum_class)
