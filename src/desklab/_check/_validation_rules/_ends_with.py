from desklab._check._validation_rules import ValidationRule


class EndsWithValidationRule(ValidationRule):

    def __init__(self, suffix: str | tuple[str, ...], variable_name: str | None = None) -> None:

        def is_valid(value: str) -> bool:
            return value.endswith(suffix)

        name = variable_name or "Value"
        message = f"{name} must end with '{suffix}'"

        super().__init__(is_valid, message)
