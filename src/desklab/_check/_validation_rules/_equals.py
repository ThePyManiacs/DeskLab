from typing import Any

from desklab._check._validation_rules import ValidationRule


class EqualsValidationRule(ValidationRule):

    def __init__(self, expected_value: Any, variable_name: str | None = None) -> None:

        def is_valid(value: Any) -> bool:
            return value == expected_value

        name = variable_name or "Value"
        message = f"{name} must be equal to {expected_value}"

        super().__init__(is_valid, message)
