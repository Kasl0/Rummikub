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

	def __str__(self):
		return "{change_type: " + self.change_type.__str__() +\
			", tile: " + self.tile.__str__() +\
			", first_position: " + self.first_position.__str__() +\
			", second_position: " + self.second_position.__str__()
