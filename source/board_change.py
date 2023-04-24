from typing import Union

from tile import Tile
from vector2d import Vector2d
from enum import Enum


class BoardChangeType(Enum):
	PLACE = 1,
	MOVE = 2,
	REMOVE = 3


class BoardChange:
	def __init__(self, change_type: BoardChangeType, tile: Union[Tile, None], first_position: Union[Vector2d, None], second_position: Union[Vector2d, None]):
		self.change_type = change_type
		self.tile = tile
		self.first_position = first_position
		self.second_position = second_position
