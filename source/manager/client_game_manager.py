from typing import Optional

from ..conection.message import MessageType
from ..logic.board import Board
from ..logic.rack import Rack
from ..conection.client import Client
from .client_actor import ClientActor
from source.gui_views.game.game_view import GameView


class ClientGameManager:
	def __init__(self, username, ip, port):
		# client - for communication with server
		self.client = Client(username, ip, port)

		self.winner = None

	def initialize_session(self):
		self.client.connect()

	def check_if_should_initialize_game(self) -> bool:
		message = self.client.receive(blocking=False)
		if not message:
			return False

		if message.type != MessageType.GAME_STARTS:
			raise ValueError(f"Expected GAME_STARTS message, received {message.type}")

		return True

	def initialize_game(self) -> Rack:
		message = self.client.receive(blocking=True)
		if message.type != MessageType.TRUE_RACK:
			raise ValueError(f"Expected TRUE_RACK message, received {message.type}")

		return message.content
