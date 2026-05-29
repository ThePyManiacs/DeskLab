# desklab/_check/_class.py
from desklab._check._parameter import parameter_validator
from typing import Callable, Any, cast


def class_validator(validation_logic: Callable[..., None]):
    def decorator(cls: type) -> type:
        for attr_name in list(cls.__dict__.keys()):
            if attr_name.startswith("__"):
                continue

            raw_attr = cls.__dict__[attr_name]

            if isinstance(raw_attr, classmethod):
                underlying_func = cast(Any, raw_attr).__func__
                is_classmethod, is_staticmethod = True, False

            elif isinstance(raw_attr, staticmethod):
                underlying_func = cast(Any, raw_attr).__func__
                is_classmethod, is_staticmethod = False, True

            else:
                underlying_func = cast(Callable[..., Any], raw_attr)
                is_classmethod, is_staticmethod = False, False

            if not callable(underlying_func):
                continue

            validator = parameter_validator(validation_logic)
            validated_func = validator(underlying_func)

            if is_classmethod:
                setattr(cls, attr_name, classmethod(validated_func))
            elif is_staticmethod:
                setattr(cls, attr_name, staticmethod(validated_func))
            else:
                setattr(cls, attr_name, validated_func)

        return cls
    return decorator
