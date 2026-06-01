from ._entity import Entity
from abc import abstractmethod
from typing import Any, Literal, Optional, Type, TypeVar, overload
from desklab.exceptions import MissingParameters


T = TypeVar("T")


class EventSensitiveEntity(Entity):
    @abstractmethod
    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        pass

    @overload
    def _get_from_kwargs(self, _type: Type[T], kwargs: dict[str, Any], _raise: Literal[True] = True) -> T:
        pass

    @overload
    def _get_from_kwargs(self, _type: Type[T], kwargs: dict[str, Any], _raise: Literal[False]) -> Optional[T]:
        pass

    def _get_from_kwargs(self, _type: Type[T], kwargs: dict[str, Any], _raise: bool = True) -> Optional[T]:
        value = kwargs.get(_type.__name__.lower())
        if not isinstance(value, _type) and _raise:
            raise MissingParameters([_type.__name__.lower()])
        return value
