from typing import Any
from typing import Any, Callable


class Check:
    def __init__(self, rule: Callable[[Any], bool], description: str | None = None) -> None:
        self.__rule = rule
        self.__description = description

    def __call__(self, *args: Any, **kwargs: Any) -> bool:
        return self.__rule(*args, **kwargs)

    def __str__(self) -> str:
        return self.__description or self.__rule.__name__
