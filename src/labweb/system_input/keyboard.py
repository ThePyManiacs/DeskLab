from typing import Optional, Set
from pygame.event import Event
from pygame.constants import (
    KEYDOWN, KEYUP, TEXTINPUT,
    KMOD_CTRL, KMOD_SHIFT, KMOD_ALT, KMOD_META
)


class KeyBoard:
    def __init__(self) -> None:
        self.__event: Optional[Event] = None
        self.__buffer: list[str] = []
        self.__pressed_keys: Set[int] = set()
        self.__mod: int = 0

    def update_event(self, event: Event):
        self.__event = event
        self.__mod = event.mod

        if event.type == KEYDOWN:
            self.__pressed_keys.add(event.key)
        elif event.type == KEYUP:
            self.__pressed_keys.discard(event.key)
        elif event.type == TEXTINPUT:
            self.__buffer.append(event.text)

    def flush(self) -> list[str]:
        buffer = self.peek()
        self.__buffer.clear()
        return buffer

    def peek(self) -> list[str]:
        return self.__buffer.copy()

    def last_input(self) -> str:
        return self.__buffer[-1]

    def key_pressed(self, key: int) -> bool:
        return key in self.__pressed_keys

    def key_down_event(self, key: int) -> bool:
        return (
            self.__event is not None and
            self.__event.type == KEYDOWN and
            self.__event.key == key
        )

    def key_up_event(self, key: int) -> bool:
        return (
            self.__event is not None and
            self.__event.type == KEYUP and
            self.__event.key == key
        )

    def ctrl_pressed(self) -> bool:
        return bool(self.__mod & KMOD_CTRL)

    def shift_pressed(self) -> bool:
        return bool(self.__mod & KMOD_SHIFT)

    def alt_pressed(self) -> bool:
        return bool(self.__mod & KMOD_ALT)

    def meta_pressed(self) -> bool:
        return bool(self.__mod & KMOD_META)

    #
