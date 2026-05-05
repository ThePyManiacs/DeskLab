from src.labweb.containers.flex_container_interface import FlexContainerInterface
from src.labweb.color import Color
from src.labweb.entities import Entity, ContainableEntity, CopiableEntity
from typing import Optional
from src.labweb.constants import VerticalAlignment, HorizontalAlignment, FlexDirection


class ProtectedFlexSlot(FlexContainerInterface):

    def __init__(self,
                 width: int,
                 height: int,
                 padding: int = 0,
                 horizontal_alignment: str | HorizontalAlignment = HorizontalAlignment.CENTER,
                 vertical_alignment: str | VerticalAlignment = VerticalAlignment.CENTER,
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 color: Color | tuple[int, int, int] | str = "BLACK",
                 bounded: bool = True) -> None:

        super().__init__(width, height, padding, 0, FlexDirection.COLUMN,
                         horizontal_alignment, vertical_alignment,
                         corners_radius, color, bounded)

    def _set_child(self, child: Entity) -> None:
        self._clear()
        self._add(child)

    def _get_child(self) -> Optional[Entity]:
        if self._is_empty():
            return None
        return self._get_children()[0]

    def copy(self) -> 'ProtectedFlexSlot':
        new_slot = self.__class__(self.get_width(),
                                  self.get_height(),
                                  self._get_padding(),
                                  self._get_horizontal_alignment(),
                                  self._get_vertical_alignment(),
                                  self.get_corners_radius(),
                                  self.get_color(),
                                  self._is_bounded())
        child = self._get_child()
        if isinstance(child, CopiableEntity):
            new_slot._set_child(child.copy())
        elif child:
            new_slot._set_child(child)
        return new_slot

    def _align(self) -> None:
        if self._is_empty():
            return
        child = self._get_child()
        if not isinstance(child, ContainableEntity):
            return

        available_width, available_height = self.__get_available_space()
        child_width, child_height = child.get_width(), child.get_height()

        if self._is_bounded():
            self.__validate_bounds(child_width, child_height,
                                   available_width, available_height)

        x = self.__calculate_horizontal_position(child_width, available_width)
        y = self.__calculate_vertical_position(child_height, available_height)

        child.set_x(x)
        child.set_y(y)

    def __get_available_space(self) -> tuple[int, int]:
        padding = self._get_padding()
        width = self.get_width() - 2 * padding
        height = self.get_height() - 2 * padding
        return width, height

    def __validate_bounds(self, child_width: int, child_height: int, available_width: int, available_height: int) -> None:
        if child_width > available_width:
            raise ValueError("ERROR: child exceeds width limit")

        if child_height > available_height:
            raise ValueError("ERROR: child exceeds height limit")

    def __calculate_horizontal_position(self, child_width: int, available_width: int) -> int:
        align = self._get_horizontal_alignment()
        base = self.get_x() + self._get_padding()

        if align == HorizontalAlignment.CENTER:
            return base + (available_width - child_width) // 2

        if align == HorizontalAlignment.RIGHT:
            return base + (available_width - child_width)

        return base

    def __calculate_vertical_position(self, child_height: int, available_height: int) -> int:
        align = self._get_vertical_alignment()
        base = self.get_y() + self._get_padding()

        if align == VerticalAlignment.CENTER:
            return base + (available_height - child_height) // 2

        if align == VerticalAlignment.BOTTOM:
            return base + (available_height - child_height)

        return base
