from typing import Any
from typing import Any, cast
from desklab.exceptions import MissingParameters
from desklab._check._validation_rules import ValidationRule
from collections.abc import Iterable


class RangeValidationRule(ValidationRule):

    def __init__(self, min_value: Any = None, max_value: Any = None, variable_name: str | None = None) -> None:

        if min_value is None and max_value is None:
            raise MissingParameters(["min_value", "max_value"],
                                    "At least one of 'min_value' or 'max_value' must be provided")

        def is_valid(value: Any) -> bool:

            if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
                iterable = cast(Iterable[Any], value)
                return all(is_valid(v) for v in iterable)

            if min_value is not None and value < min_value:
                return False

            if max_value is not None and value > max_value:
                return False

            return True

        name = variable_name or "Value"

        if min_value is not None and max_value is not None:
            message = f"{name} must be between {min_value} and {max_value}"

        elif min_value is not None:
            message = f"{name} must be greater than or equal to {min_value}"

        else:
            message = f"{name} must be less than or equal to {max_value}"

        super().__init__(is_valid, message)
