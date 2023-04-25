from enum import Enum


class MessageType(Enum):
	# server message types
	PLAYER_JOINED = 101,
	GAME_STARTS = 102,
	TILE = 103,
	NEXT_TURN = 104,
	TRUE_BOARD = 105,
	TRUE_RACK = 106,
	GAME_ENDS = 107,

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
		return "{\n" +\
				"\tmessage_type: " + str(self.type) +\
				",\n\tcontent: " + str(self.content) +\
				"\n}"
