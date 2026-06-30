from typing import Any


class DeskLabError(Exception):
    pass


class LogicError(DeskLabError):
    pass


class InvalidParameterValue(DeskLabError, ValueError):
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
        error = f"Children exceeded bounds in '{container_name}'"
        super().__init__(error)


class FileReadingError(DeskLabError):
    def __init__(self, file_path: str, *args: Any) -> None:
        error = f"An error ocurred while reading the file at '{file_path}'"
        super().__init__(error, *args)


class BytesReadingError(DeskLabError):
    def __init__(self, description: str, *args: Any) -> None:
        error = f"An error ocurred while reading bytes data: {description}"
        super().__init__(error, *args)
