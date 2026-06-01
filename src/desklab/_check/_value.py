import inspect
from typing import Callable, TypeVar, ParamSpec
from functools import wraps
from desklab.exceptions import InvalidParameterValue
from desklab._check._check_operations import Check


P = ParamSpec("P")
R = TypeVar("R")


def value_check(**validations: Check) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        signature = inspect.signature(function)

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound_arguments = signature.bind(*args, **kwargs)
            bound_arguments.apply_defaults()

            for param_name, param_value in bound_arguments.arguments.items():
                if param_name in ("self", "cls"):
                    continue
                validation_rule = validations.get(param_name)
                if validation_rule is not None and not validation_rule(param_value):
                    raise InvalidParameterValue(param_name, param_value,
                                                str(validation_rule))

            return function(*args, **kwargs)
        return wrapper
    return decorator
