from src.labweb.system.mouse import Mouse
from src.labweb.color import Color
from src.labweb.entities import EventSensitiveEntity
from src.labweb.area import Area
from typing import Any, Callable


class EventListener(EventSensitiveEntity):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.set_actions(actions)
        self.set_condition(condition)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        if self._trigger_condition(*args, **kwargs):
            self._trigger_actions(*args, **kwargs)

    def get_condition(self) -> Callable[..., bool]:
        return self.__condition

    def set_condition(self, condition: Callable[..., bool]) -> None:
        self.__condition = condition

    def get_actions(self) -> list[Callable[..., Any]]:
        return self.__action

    def set_actions(self, action: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        if isinstance(action, list):
            self.__action = action
            return
        self.__action: list[Callable[..., Any]] = [action]

    def _trigger_condition(self, *args: Any, **kwargs: Any) -> bool:
        condition = self.get_condition()
        try:
            return condition(*args, **kwargs)
        except TypeError:
            return condition()

    def _trigger_actions(self, *args: Any, **kwargs: Any) -> None:
        for action in self.get_actions():
            try:
                action(*args, **kwargs)
            except TypeError:
                return action()


class FirstTimeEventListener(EventListener):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.__has_triggered = False
        super().__init__(condition, actions)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        if not self.__has_triggered and self._trigger_condition(*args, **kwargs):
            self._trigger_actions(*args, **kwargs)
            self.__has_triggered = True


class ChangeEventListener(EventListener):

    def __init__(self, condition: Callable[..., bool], actions: Callable[..., Any] | list[Callable[..., Any]]) -> None:
        self.__previous_state = None
        super().__init__(condition, actions)

    def handle_event(self, *args: Any, **kwargs: Any) -> None:
        condition_value = self._trigger_condition(*args, **kwargs)
        if self.__previous_state is not None and condition_value != self.__previous_state:
            self._trigger_actions(*args, **kwargs)

        self.__previous_state = condition_value


class HoverColorEventListener(ChangeEventListener):

    def __init__(self, area: Area, hover_color: Color | tuple[int, int, int] | str) -> None:
        self.__area = area
        self.__default_color = area.get_color()
        self.__hover_color = hover_color
        super().__init__(self.__area_contains_mouse_position, self.__change_area_color)

    def __area_contains_mouse_position(self, *args: Any, **kwargs: Any) -> bool:
        mouse = kwargs.get("mouse")
        if not isinstance(mouse, Mouse):
            self._raise_for_missing_parameter("mouse", Mouse.__name__)
        return self.__area.contains(mouse.get_position())

    def __change_area_color(self) -> None:
        if self.__area.get_color() == self.__default_color:
            self.__area.set_color(self.__hover_color)
            return
        self.__area.set_color(self.__default_color)
