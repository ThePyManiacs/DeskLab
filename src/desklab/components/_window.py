# fmt: off
import sys
from pygame._sdl2 import Window as PygameWindow
from desklab.system import Mouse, KeyBoard, ClipBoard
from desklab.containers import FlexBox, FlexDirection, HorizontalAlignment, VerticalAlignment
from desklab.primitives import Color
from pygame.locals import QUIT
from typing import Any, Iterable
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from importlib import resources
# fmt: on


class Window:

    __is_set_up = False

    def __init__(self) -> None:
        if not self.__is_set_up:
            self.setup()
        self.__layers: list[FlexBox] = []
        self.__layer_surfaces: list[pygame.Surface] = []

    @classmethod
    def setup(cls, width: int = 640, height: int = 480, caption: str = "DeskLab", icon: str | None = None) -> None:
        if icon is None:
            assets = resources.files('desklab._assets')
            icon_path = assets.joinpath('desklab.png')

            with resources.as_file(icon_path) as desklab_icon:
                icon = str(desklab_icon)

        pygame.display.set_icon(pygame.image.load(icon))
        pygame.init()
        cls.__screen = pygame.display.set_mode((width, height))
        cls.__clock = pygame.time.Clock()
        cls.__width = width
        cls.__height = height
        pygame.display.set_caption(caption)
        cls.__is_set_up = True
        cls.__window = PygameWindow.from_display_module()

    def add_layer(self,
                  padding: int = 0,
                  space_between: int = 0,
                  flex_direction: str | FlexDirection = FlexDirection.COLUMN,
                  horizontal_alignment: str | HorizontalAlignment = HorizontalAlignment.CENTER,
                  vertical_alignment: str | VerticalAlignment = VerticalAlignment.CENTER,
                  color: Color | tuple[int, ...] | str = "BLACK",
                  visible: bool = True) -> FlexBox:

        layer = FlexBox(self.__width, self.__height, padding, space_between,
                        flex_direction, horizontal_alignment, vertical_alignment,
                        color=color, visible=visible)
        self.__layers.append(layer)
        surface = pygame.Surface(
            (self.__width, self.__height), pygame.SRCALPHA)
        self.__layer_surfaces.append(surface)
        return layer

    def get_layer(self, index: int) -> FlexBox:
        return self.__layers[index]

    def __get_window_coordinates(self):
        window_coordinates = self.__window.position
        assert isinstance(window_coordinates, Iterable)
        return tuple(window_coordinates)

    def open(self) -> None:

        mouse = Mouse()
        keyboard = KeyBoard()
        clipboard = ClipBoard()
        self.__running = True
        while self.__running:
            mouse.update_refference_origin(
                *self.__get_window_coordinates())

            if events := pygame.event.get():
                for event in events:

                    keyboard.update_event(event)
                    mouse.update_event(event)

                    if event.type == QUIT:
                        sys.exit()

                    self.__handle_event(event=event, mouse=mouse,
                                        keyboard=keyboard,
                                        clipboard=clipboard,
                                        screen=self.__screen)
            else:
                keyboard.update_event(None)
                mouse.update_event(None)
                self.__handle_event(mouse=mouse,
                                    keyboard=keyboard,
                                    clipboard=clipboard,
                                    screen=self.__screen)

            self.__screen.fill((0, 0, 0))
            self.__display_layers()

            pygame.display.update()
            self.__clock.tick(60)

    def close(self) -> None:
        self.__running = False

    def __handle_event(self, *args: Any, **kwargs: Any):
        if not self.__layers:
            return
        self.__layers[-1].handle_event(*args, **kwargs)

    def __display_layers(self):
        for layer, surface in zip(self.__layers, self.__layer_surfaces):
            surface.fill((0, 0, 0, 0))
            layer.display(surface)
            self.__screen.blit(surface, (0, 0))
