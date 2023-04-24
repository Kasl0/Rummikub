from typing import Dict

from server import Server
from rack import Rack
from message import Message, MessageType
from server_actor import ServerActor
from tile_pool import TilePool


class ServerGame:
	def __init__(self):
		self.server = Server()

		# game initialization
		self.tile_pool = TilePool()

		# dictionary of clients' racks
		# key - assigned client id
		# value - his rack
		self.racks: Dict[int, Rack] = {}

		self.winner = None

	def play(self):
		"""Go through all game stages:\n
				1. initialise server + let players join,\n
				2. initialise game,\n
				3. host main game part,\n
				4. end game + disconnect players + turn off the server"""

		print("Initialising server")
		self.stage1()
		print("Server initialised")

		print("Drawing starting tiles and sending them to players")
		self.stage2()
		print("All starting racks sent")

		print("Main game part starts!")
		self.stage3()
		print("We have a winner")

		print("Closing server")
		self.stage4()

		return

	def stage1(self):
		"""Initialise server and wait for players to join"""
		self.server.start()  # wait for all players to join
		self.server.send_all(Message(MessageType.GAME_STARTS, "Starting game"))

	def stage2(self):
		"""Initialise game: create tile rack for all players and send them their initial tiles"""
		for client_id in self.server.clients.keys():
			self.racks[client_id] = Rack()

			for i in range(14):
				self.racks[client_id].add_tile(self.tile_pool.draw_random_tile())

			self.server.send(client_id, Message(MessageType.TRUE_RACK, self.racks[client_id]))

	def stage3(self):
		"""Main game part loop. Players take turns and perform actions"""
		server_actor = ServerActor(self.racks, self.tile_pool, self.server)
		self.winner = server_actor.serve_main_game_part()  # enter main part of the game

	def stage4(self):
		"""End game, disconnect players, turn off the server"""
		winner_username = self.server.clients[self.winner][2]
		self.server.send_all(Message(MessageType.GAME_ENDS, winner_username))
		self.server.close()
		pass
