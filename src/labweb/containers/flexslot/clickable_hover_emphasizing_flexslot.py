from typing import Any

from src.labweb.color import Color
from src.labweb.constants import HorizontalAlignment, VerticalAlignment
from src.labweb.containers.flexslot.protected_flexslot import ProtectedFlexSlot
from src.labweb.area import ClickableArea, HoverEmphasizingArea


class ClickableHoverEmphasizingFlexSlot(ProtectedFlexSlot, ClickableArea, HoverEmphasizingArea):

    def __init__(self,
                 width: int,
                 height: int,
                 padding: int = 0,
                 horizontal_alignment: str | HorizontalAlignment = "CENTER",
                 vertical_alignment: str | VerticalAlignment = "CENTER",
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 color: Color | tuple[int, int, int] | str = "BLACK",
                 hover_emphasis_intensity: int = 100,
                 bounded: bool = True, *args: Any, **kwargs: Any) -> None:
        super().__init__(width=width,
                         height=height,
                         padding=padding,
                         horizontal_alignment=horizontal_alignment,
                         vertical_alignment=vertical_alignment,
                         corners_radius=corners_radius,
                         color=color,
                         hover_emphasis_intensity=hover_emphasis_intensity,
                         bounded=bounded, *args, **kwargs)

    def copy(self) -> "ClickableHoverEmphasizingFlexSlot":
        new_instance = self.__class__(self.get_width(), self.get_height(),
                                      self._get_padding(), self._get_horizontal_alignment(),
                                      self._get_vertical_alignment(), self.get_corners_radius(),
                                      self.get_color(), self.get_emphasis_intensity(), self._is_bounded())
        self._migrate_children(new_instance)
        return new_instance
