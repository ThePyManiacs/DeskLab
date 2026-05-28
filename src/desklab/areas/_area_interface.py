from desklab.entity_types import ContainableEntity, DisplayableEntity, CopiableEntity, ColorableEntity
from desklab.primitives import Color
from abc import abstractmethod


class AreaInterface(ContainableEntity, DisplayableEntity, ColorableEntity, CopiableEntity):

    def __init__(self, width: int, height: int, color: Color | tuple[int, ...] | str = "BLACK") -> None:
        super().__init__(x=0, y=0, width=width, height=height, color=color)

    @abstractmethod
    def contains(self, coordinates: tuple[int, int]) -> bool:
        pass

    def get_rect(self) -> tuple[int, int, int, int]:
        return (self.get_x(), self.get_y(),
                self.get_width(), self.get_height())
