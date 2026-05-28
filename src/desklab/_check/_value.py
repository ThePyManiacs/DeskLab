from typing import Any
from typing import Any
from desklab.exceptions import InvalidParameterValue
from desklab._check._parameter import parameter_validator
from desklab._check._validation_rules import ValidationRule


def value_check(**validations: ValidationRule):
    def _value_check_logic(param_name: str, param_value: Any, **kwargs: Any):
        validation_rule = validations.get(param_name)
        if validation_rule is not None and not validation_rule(param_value):
            raise InvalidParameterValue(param_name, param_value,
                                        str(validation_rule))
    return parameter_validator(_value_check_logic)
