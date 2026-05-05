from typing import Optional

from src.labweb.constants import HorizontalAlignment, VerticalAlignment
from src.labweb.entities import Entity
from src.labweb.containers.protected_flexslot import ProtectedFlexSlot


class FlexSlot(ProtectedFlexSlot):

    def pop(self) -> Optional[Entity]: return self._pop()
    def clear(self) -> None: self._clear()
    def is_empty(self) -> bool: return self._is_empty()
    def is_bounded(self) -> bool: return self._is_bounded()
    def switch_direction(self) -> None: self._switch_direction()

    def get_horizontal_alignment(self) -> HorizontalAlignment:
        return self._get_horizontal_alignment()

    def get_vertical_alignment(self) -> VerticalAlignment:
        return self._get_vertical_alignment()

    def set_horizontal_alignment(self, horizontal_alignment: HorizontalAlignment = HorizontalAlignment.CENTER) -> None:
        self._set_horizontal_alignment(horizontal_alignment)

    def set_vertical_alignment(self, vertical_alignment: VerticalAlignment = VerticalAlignment.CENTER) -> None:
        self._set_vertical_alignment(vertical_alignment)
