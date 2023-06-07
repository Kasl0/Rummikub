from ..logic.board import Board
from ..logic.rack import Rack
from ..conection.client import Client
from .client_actor import ClientActor
from source.gui_views.game.game_view import GameView


class ClientGameManager:
	def __init__(self, username, ip, port):
		# client - for communication with server
		self.client = Client(username, ip, port)

		# player's board and rack
		self.board = Board()
		self.rack = Rack()

		self.winner = None

	def initialize_session(self):
		self.client.connect()

	def initialize_game(self):
		self.rack = self.client.receive(blocking=True).content
		print("Rack from the server:", self.rack)
		return GameView(ClientActor(self.board, self.rack, self.client))

	def end_game(self):
		print("The winner is: " + str(self.winner))
		self.client.close_connection()
		pass
