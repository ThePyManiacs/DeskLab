from typing import Any, Type


class DeskLabError(Exception):
    pass


class InvalidDecorationTarget(DeskLabError):
    def __init__(self, decorator_name: str, expected_target_type: Type[Any] | list[Type[Any]], target: Any) -> None:
        if isinstance(expected_target_type, list):
            expected_target_types = [t.__name__ for t in expected_target_type]
        else:
            expected_target_types = [expected_target_type.__name__]
        error = f"@{decorator_name} can only be applied to {expected_target_types}, but got {type(target).__name__}"
        super().__init__(error)


class InvalidParameterType(DeskLabError):
    def __init__(self, parameter_name: str, expected_type: Type[Any], received_type: Type[Any]) -> None:

        expected_repr = self.__get_type_representation(expected_type)
        received_repr = self.__get_type_representation(received_type)

        mensagem = (
            f"Invalid type for parameter '{parameter_name}'. "
            f"Expected type: {expected_repr}, "
            f"Received type: {received_repr}."
        )
        super().__init__(mensagem)

    def __get_type_representation(self, _type: Type[Any]) -> str:
        if hasattr(_type, "__name__"):
            return _type.__name__
        return str(_type)


class InvalidParameterValue(DeskLabError):
    def __init__(self, parameter_name: str, parameter_value: Any, rule: str = "") -> None:
        error = f"Invalid value {parameter_value!r} for '{parameter_name}'"
        if rule:
            error += f" (Rule: {rule})"
        super().__init__(error)


class MissingParameters(DeskLabError):
    def __init__(self, parameter_names: list[str], *args: Any, **kwargs: Any) -> None:
        error = f"Missing required parameters: {', '.join(parameter_names)}"
        super().__init__(error, *args, **kwargs)


class ContainerBoundsExceeded(DeskLabError):
    def __init__(self, container_name: str) -> None:
        error = f"Children exceeded bounds limit in '{container_name}'"
        super().__init__(error)


class FileReadingError(DeskLabError):
    def __init__(self, file_path: str, *args: Any) -> None:
        error = f"An error ocurred while reading the file at '{file_path}'"
        super().__init__(error, *args)


class BytesReadingError(DeskLabError):
    def __init__(self, description: str, *args: Any) -> None:
        error = f"An error ocurred while reading bytes data: {description}"
        super().__init__(error, *args)
