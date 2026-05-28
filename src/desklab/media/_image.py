# fmt: off
from typing import Any

from PIL import Image as PilImage
import numpy as np
from desklab.entity_types import DisplayableEntity, ContainableEntity, CopiableEntity
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import Surface
from desklab._check import type_check, value_check, EndsWithValidationRule, EqualsValidationRule
# fmt: on

_valid_image_formats = (".png", ".jpg", ".jpeg", ".bmp", ".gif")


@type_check
class Image(DisplayableEntity, ContainableEntity, CopiableEntity):

    def __init__(self, image: str | np.ndarray) -> None:
        self.__set_image_surface(image)
        super().__init__(width=self.get_matrix().shape[0],
                         height=self.get_matrix().shape[0])

    def get_matrix(self) -> np.ndarray: return self.__image_matrix

    @value_check(image_path=EndsWithValidationRule(_valid_image_formats, f"Image format must be one of {_valid_image_formats}"))
    def __extract_image_data_from_path(self, image_path: str) -> np.ndarray:
        img = PilImage.open(image_path).convert("RGB")
        return np.array(img)

    @value_check(image_ndim=EqualsValidationRule(3, "Image must have 3 dimensions"),
                 image_color_channels=EqualsValidationRule(3, "Image must have 3 color channels"))
    def __validate_dimensions(self, image_ndim: int, image_color_channels: int) -> None:
        pass

    def __set_image_surface(self, image: str | np.ndarray) -> None:

        if isinstance(image, str):
            image = self.__extract_image_data_from_path(image)

        self.__validate_dimensions(image.ndim, image.shape[2])
        image = np.transpose(image, (1, 0, 2))
        image = np.ascontiguousarray(image)

        self.__image_matrix = image
        self.__image_surface = pygame.surfarray.make_surface(image)

    def rescale(self, width: int, height: int) -> None:
        self.__image_surface = pygame.transform.scale(
            self.__image_surface, (width, height))
        self._set_width(width)
        self._set_height(height)

    def display(self, screen: Surface) -> None:
        screen.blit(self.__image_surface, (self.get_x(), self.get_y()))

    def _get_copy_replacement_map(self) -> dict[str, Any]:
        return {"image": self.get_matrix().copy()}
