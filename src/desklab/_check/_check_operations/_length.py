from typing import Any

from desklab._check._check_operations import Check
from desklab.exceptions import InvalidParameterValue


class CheckLength(Check):

    def __init__(self, reference_length: int, comparison: str = "=", variable_name: str | None = None) -> None:

        operators = {"=", ">", "<", ">=", "<="}
        if comparison not in operators:
            raise InvalidParameterValue(f"comparison", comparison,
                                        f"'comparison' must be one of: {operators}")

        def compare(value: Any) -> bool:
            if comparison == "=":
                return len(value) == reference_length
            elif comparison == ">":
                return len(value) > reference_length
            elif comparison == "<":
                return len(value) < reference_length
            elif comparison == ">=":
                return len(value) >= reference_length
            elif comparison == "<=":
                return len(value) <= reference_length
            raise InvalidParameterValue(f"comparison", comparison,
                                        f"'comparison' must be one of: {operators}")

        name = variable_name or "Value"
        message = f"length({name}) {comparison} {reference_length}"

        super().__init__(compare, message)
