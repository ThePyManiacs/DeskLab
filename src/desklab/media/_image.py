# fmt: off
import os
from typing import Any, Self, overload
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import Surface
from desklab.entity_types import DisplayableEntity, ContainableEntity, CopiableEntity
from desklab._check import value_check, CheckRange
# fmt: on


class Image(DisplayableEntity, ContainableEntity, CopiableEntity):

    @overload
    def __init__(self, image_source: str) -> None: ...

    @overload
    def __init__(self, image_source: Surface) -> None: ...

    def __init__(self, image_source: str | Surface) -> None:
        self.__load_surface(image_source)

        super().__init__(
            width=self.__image_surface.get_width(),
            height=self.__image_surface.get_height()
        )

    def __load_surface(self, source: str | Surface) -> None:
        if isinstance(source, Surface):
            self.__image_surface = source.copy()
        else:
            self.__image_surface = pygame.image.load(source)

        if self.__image_surface.get_alpha() is not None or self.__image_surface.get_masks()[3] != 0:
            self.__image_surface = self.__image_surface.convert_alpha()
        else:
            self.__image_surface = self.__image_surface.convert()

    def __get_surface(self) -> Surface:
        return self.__image_surface.copy()

    @value_check(percentage=CheckRange(0, variable_name="percentage"))
    def rescaled(self, percentage: float) -> Self:
        new_width = int(self.get_width() * percentage)
        new_height = int(self.get_height() * percentage)
        new_surface = pygame.transform.scale(self.__get_surface(),
                                             (new_width, new_height))
        return self.copy(image_source=new_surface)

    @value_check(width=CheckRange(0, variable_name="width"),
                 height=CheckRange(0, variable_name="height"))
    def resized(self, width: int, height: int) -> Self:
        new_surface = pygame.transform.scale(self.__get_surface(),
                                             (width, height))
        return self.copy(image_source=new_surface)

    def display(self, screen: Surface) -> None:
        screen.blit(self.__image_surface, (self.get_x(), self.get_y()))

    def _get_copy_replacement_map(self) -> dict[str, Any]:
        return {"image_source": self.__get_surface()}
