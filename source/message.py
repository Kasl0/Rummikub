from enum import Enum


class MessageType(Enum):
	# server message types
	PLAYER_JOINED = 101,
	GAME_STARTS = 102,
	TILE = 103,
	NEXT_TURN = 104,
	END_TURN = 105,
	TRUE_BOARD = 106,
	TRUE_RACK = 107,
	GAME_ENDS = 108,

	# client message types
	JOIN = 201,
	CONFIRM_CHANGES = 202,
	DRAW_TILE = 203,
	REVERT_CHANGES = 204,

	# universal message types
	OK = 301,
	NOT_OK = 302,
	CHANGE_INTRODUCED = 303,


class Message:
	def __init__(self, message_type: MessageType, content: any):
		self.type = message_type
		self.content = content

	def __str__(self):
		return "{message_type: " + str(self.type) + ", content: " + str(self.content) + "}"
