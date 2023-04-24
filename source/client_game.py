from board import Board
from rack import Rack
from client import Client
from client_actor import ClientActor


class ClientGame:
	def __init__(self):
		# client - for communication with server
		self.client = Client()

		# player's board and rack
		self.board = Board()
		self.rack = Rack()

		self.winner = None

	def play(self):
		"""Go through all game stages:\n
				1. join server,\n
				2. receive starting tiles,\n
				3. play main game part,\n
				4. end game sequence + disconnect from server"""

		print("Connecting with server")
		self.stage1()
		print("Success")

		print("Receive starting tiles from the server")
		self.stage2()
		print("All tiles received")

		print("Main game part starts!")
		self.stage3()
		# print("We have a winner")

		print("Closing connection with server")
		self.stage4()

		return

	def stage1(self):
		"""Connect with server and join a session"""
		self.client.connect()
		print("Server:", self.client.receive().content)  # Client waits for starting game signal

	def stage2(self):
		"""Game initialisation - receive starting tiles from server"""

		message = self.client.receive()
		self.rack = message.content
		print("Rack from the server:", self.rack)

	def stage3(self):
		"""Main game part loop"""

		player = ClientActor(self.board, self.rack, self.client)
		self.winner = player.play_main_game_part()  # from now on object of class Player plays the main part of game

	def stage4(self):
		"""End game, disconnect players, turn off the server"""
		print("The winner is: " + str(self.winner))
		self.client.close_connection()
		pass
