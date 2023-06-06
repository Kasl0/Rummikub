from ..logic.board import Board
from ..logic.rack import Rack
from ..conection.client import Client
from .client_actor import ClientActor
from ..gui_game.game import Game


class ClientGameManager:
	def __init__(self, username, ip, port):
		# client - for communication with server
		self.client = Client(username, ip, port)

		# player's board and rack
		self.board = Board()
		self.rack = Rack()

		self.winner = None

	"""def play(self):
		"Go through all game stages:\n
				1. join server,\n
				2. receive starting tiles,\n
				3. play main game part,\n
				4. end game sequence + disconnect from server"

		print("Connecting with server")
		self.session_initialization()
		print("Success")

		print("Receive starting tiles from the server")
		self.game_initialization()
		print("All tiles received")

		print("Main game part starts!")
		self.main_game()
		# print("We have a winner")

		print("Closing connection with server")
		self.end_game()

		return"""

	def initialize_session(self):
		self.client.connect()

	def initialize_game(self):
		self.rack = self.client.receive(blocking=True).content
		print("Rack from the server:", self.rack)
		return Game(ClientActor(self.board, self.rack, self.client))

	"""def main_game(self):
		player = ClientActor(self.board, self.rack, self.client)
		# self.winner = player.play_main_game_part()  # from now on object of class Player plays the main part of game"""

	def end_game(self):
		print("The winner is: " + str(self.winner))
		self.client.close_connection()
		pass
