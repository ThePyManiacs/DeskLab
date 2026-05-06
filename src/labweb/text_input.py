from typing import Any

from src.labweb.color import Color
from src.labweb.containers.protected_flexslot import ProtectedFlexSlot
from src.labweb.containers.flexbox import FlexBox
from src.labweb.containers.clickable_flexbox import ClickableFlexBox


class _TextInputCell(ClickableFlexBox):

    def __init__(self, width: int, height: int, color: Color | tuple[int, int, int] | str = "BLACK") -> None:
        super().__init__(width, height, 0, 0, "ROW", "CENTER", "CENTER", 0, color, 0, True)

    def handle_event(self, *args: Any, **kwargs: Any):
        pass


class TextInput(ProtectedFlexSlot):

    __HORIZONTAL_PADDING_PERCENTAGE = 5
    __VERTICAL_PADDING_PERCENTAGE = 33

    def __init__(self,
                 width: int,
                 height: int,
                 corners_radius: tuple[int, int, int, int] | int = 0,
                 background_color: Color | tuple[int,
                                                 int, int] | str = "BLACK",
                 text_color: Color | tuple[int, int, int] | str = "BLACK") -> None:

        super().__init__(width, height, 0, "CENTER", "CENTER",
                         corners_radius, background_color, True)
        self.__set_text_container()

    def set_text_color(self, color: Color | tuple[int, int, int] | str = "BLACK"):
        self.__text_color = color if isinstance(color, Color) else Color(color)

    def get_text_color(self) -> Color:
        return self.__text_color

    def __set_text_container(self, ) -> None:
        self.__text_container = FlexBox(self.get_width() - self.__calcuate_horizontal_padding(),
                                        self.get_height() - self.__calculate_vertical_padding(),
                                        0, 0, "ROW", "LEFT", "CENTER", 0, self.get_color(), True)
        self._add(self.__text_container)

    def __calcuate_horizontal_padding(self) -> int:
        return self.__HORIZONTAL_PADDING_PERCENTAGE*self.get_width()//100

    def __calculate_vertical_padding(self) -> int:
        return self.__VERTICAL_PADDING_PERCENTAGE*self.get_height()//100
