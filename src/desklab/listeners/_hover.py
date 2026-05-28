from desklab.system import Mouse
from desklab.areas import AreaInterface
from typing import Any, Callable
from ._protected_listener import ProtectedListener


class HoverListener(ProtectedListener):

    def __init__(self,
                 area: AreaInterface,
                 actions: Callable[..., Any] | list[Callable[..., Any]],
                 aditional_conditions: Callable[...,
                                                Any] | list[Callable[..., Any]] = [],
                 on_change: bool = False,
                 listen_once: bool = False) -> None:

        self.__area = area

        if isinstance(aditional_conditions, Callable):
            aditional_conditions = [aditional_conditions]

        super().__init__([self.__hover, *aditional_conditions],
                         actions, on_change, listen_once)

    def __hover(self, *args: Any, **kwargs: Any) -> bool:
        mouse = self._get_from_kwargs(Mouse, kwargs)
        return self.__area.contains(mouse.get_position())

    def _get_copy_replacement_map(self) -> dict[str, Any]:
        return {
            "area": self.__area,
            "actions": self._get_actions(),
            "aditional_conditions": self._get_conditions()[1:],
            "on_change": self._on_change,
            "listen_once": self._listen_once
        }
