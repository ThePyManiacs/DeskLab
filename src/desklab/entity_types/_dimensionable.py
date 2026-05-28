from ._entity import Entity
from typing import Any
from desklab._check import type_check, value_check, RangeValidationRule


@type_check
class DimensionableEntity(Entity):

    def __init__(self, width: int = 0, height: int = 0, **kwargs: Any):
        super().__init__(**kwargs)
        self._set_width(width)
        self._set_height(height)

    @value_check(width=RangeValidationRule(min_value=0, variable_name="width"))
    def _set_width(self, width: int):
        self.__width = width

    def get_width(self) -> int:
        return self.__width

    @value_check(height=RangeValidationRule(min_value=0, variable_name="height"))
    def _set_height(self, height: int):
        self.__height = height

    def get_height(self) -> int:
        return self.__height
