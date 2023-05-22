from time import sleep
from typing import Dict

from ..conection.server import Server
from ..logic.rack import Rack
from ..conection.message import Message, MessageType
from .server_actor import ServerActor
from ..logic.tile_pool import TilePool


class ServerGameManager:
	def __init__(self, port):
		self.server = Server(port)

		# game initialization
		self.tile_pool = TilePool()

		# dictionary of clients' racks
		# key - assigned client id
		# value - his rack
		self.racks: Dict[int, Rack] = {}

		self.server_actor = ServerActor(self.racks, self.tile_pool, self.server)

		self.winner_client_id = None

	# def play(self):
	# 	"""Go through all game stages:\n
	# 			1. initialise server and session + let players join,\n
	# 			2. initialise game,\n
	# 			3. host main game part,\n
	# 			4. end game + disconnect players + turn off the server"""
	#
	# 	print("Initialising server")
	# 	self.session_initialization()
	# 	print("Server initialised")
	#
	# 	print("Drawing starting tiles and sending them to players")
	# 	self.game_initialization()
	# 	print("All starting racks sent")
	#
	# 	print("Main game part starts!")
	# 	self.main_game()
	# 	print("We have a winner")
	#
	# 	print("Closing server")
	# 	self.end_game()
	#
	# 	return

	def session_initialization(self):
		self.server.send_all(Message(MessageType.GAME_STARTS, "Starting game"))

	def game_initialization(self):
		sleep(1)  # TODO: Not very professional (but works)
		for client_id in self.server.clients.get_client_ids():
			self.racks[client_id] = Rack()

			for i in range(14):
				self.racks[client_id].add_tile(self.tile_pool.draw_random_tile())

			self.server.send(client_id, Message(MessageType.TRUE_RACK, self.racks[client_id]))
		self.server_actor.start_next_turn()

	def update_main_game(self):
		print("update_main_game")
		return self.server_actor.update_main_game()  # enter main part of the game

	def end_game(self):
		print("The winner is: " + str(self.winner_client_id))
		winner_client_username = self.server.clients.get_username(self.winner_client_id)
		self.server.send_all(Message(MessageType.GAME_ENDS, winner_client_username))
		self.server.close()
		pass
