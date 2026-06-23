from desklab._check import value_check, Check, CheckRange
from typing import Literal, Self
import colorsys

_color_map: dict[str, tuple[int, ...]] = {
    "BLACK": (0, 0, 0, 1),
    "DARK_GRAY": (64, 64, 64, 1),
    "GRAY": (128, 128, 128, 1),
    "LIGHT_GRAY": (192, 192, 192, 1),
    "WHITE": (255, 255, 255, 1),
    "MAROON": (128, 0, 0, 1),
    "RED": (255, 0, 0, 1),
    "BROWN": (165, 42, 42, 1),
    "ORANGE": (255, 165, 0, 1),
    "GOLD": (255, 215, 0, 1),
    "YELLOW": (255, 255, 0, 1),
    "OLIVE": (128, 128, 0, 1),
    "LIME": (0, 255, 0, 1),
    "GREEN": (0, 255, 0, 1),
    "TEAL": (0, 128, 128, 1),
    "TURQUOISE": (64, 224, 208, 1),
    "CYAN": (0, 255, 255, 1),
    "NAVY": (0, 0, 128, 1),
    "BLUE": (0, 0, 255, 1),
    "INDIGO": (75, 0, 130, 1),
    "PURPLE": (128, 0, 128, 1),
    "MAGENTA": (200, 0, 100, 1),
    "VIOLET": (238, 130, 238, 1),
    "PINK": (255, 192, 203, 1),
    "SILVER": (192, 192, 192, 1),
}


class Color:

    __DEFAULT_DELTA = 5

    def __init__(self, color: tuple[int, ...] | str) -> None:
        self.__set_color(color)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.get_tuple() == other.get_tuple()
        elif isinstance(other, str):
            return self == self.__class__(other)
        return NotImplemented

    def copy(self) -> Self:
        return self.__class__(self.get_tuple())

    @value_check(color=Check(lambda c: c.upper() in _color_map, f"Valid colors are {list(_color_map.keys())}"))
    def __search_tuple(self, color: str) -> tuple[int, ...]:
        return _color_map[color.upper().strip()]

    @value_check(channel=CheckRange(0, 255, variable_name="color channel"))
    def __validate_range(self, channel: int) -> None:
        pass

    @value_check(length=CheckRange(3, 4, variable_name="color tuple"))
    def __validate_length(self, length: int) -> None:
        pass

    def __set_color(self, color: tuple[int, ...] | str):
        if isinstance(color, str):
            color = self.__get_tuple_from_color_name(color)
        self.__set_tuple(color)

    def __set_tuple(self, color: tuple[int, ...]):
        self.__validate_length(len(color))
        if len(color) == 3:
            color = (*color, 1)
        for channel in color:
            self.__validate_range(channel)
        self.__tuple = color

    def __get_tuple_from_color_name(self, color: str) -> tuple[int, ...]:

        positive_count = color.count("+")
        negative_count = color.count("-")
        raw_color = color.replace("+", "").replace("-", "")
        color_tuple = self.__search_tuple(raw_color)

        for _ in range(positive_count):
            color_tuple = self.__alter_brightness(self.__DEFAULT_DELTA, "+")
        for _ in range(negative_count):
            color_tuple = self.__alter_brightness(self.__DEFAULT_DELTA, "-")
        return color_tuple

    @value_check(operation=Check(lambda op: op in ["+", "-"], "Operation must be either '+' or '-'"))
    def __alter_brightness(self, intensity: int, operation: Literal["+", "-"]) -> tuple[int, ...]:

        r, g, b, a = self.__tuple

        r /= 255
        g /= 255
        b /= 255

        hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
        amount = intensity / 100

        if operation == "+":
            lightness += (1 - lightness) * amount
        else:
            lightness *= (1 - amount)

        lightness = max(0, min(1, lightness))
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)

        return (int(r * 255), int(g * 255), int(b * 255), a)

    def get_luminance(self) -> float:
        r, g, b, _ = self.__tuple
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def luminance_emphasized(self, intensity: int = 100) -> "Color":
        lum = self.get_luminance()

        if lum < 128:
            factor = (128 - lum) / 128
            return self.lightened(int((40 + 60 * factor) * (intensity / 100)))
        else:
            factor = (lum - 128) / 127
            return self.darkened(int((30 + 70 * factor) * (intensity / 100)))

    def lightened(self, intensity: int) -> 'Color':
        new_tuple = self.__alter_brightness(intensity, "-")
        return Color(new_tuple)

    def darkened(self, intensity: int) -> 'Color':
        new_tuple = self.__alter_brightness(intensity, "+")
        return Color(new_tuple)

    def with_alpha(self, alpha: int) -> 'Color':
        r, g, b, _ = self.__tuple
        return Color((r, g, b, alpha))

    def get_tuple(self) -> tuple[int, ...]:
        return self.__tuple

    @classmethod
    def get_options(cls) -> list[str]:
        return list(_color_map.keys())
