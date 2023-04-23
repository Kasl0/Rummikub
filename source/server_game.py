from time import sleep
from typing import Dict

from server import Server
from board import Board
from rack import Rack
from message import Message, MessageType
from tile_pool import TilePool


class ServerGame:
	server: Server
	tile_pool = TilePool()
	board = Board()

	# dictionary of clients' racks
	# key - assigned client id
	# value - his rack
	racks: Dict[int, Rack] = {}

	def __init__(self):
		# server and session creation
		self.server = Server()

		# game initialization
		self.tile_pool = TilePool()

	def play(self):
		"""Go through all game stages:\n
				1. initialise server + let players join,\n
				2. initialise game,\n
				3. host proper game,\n
				4. end game + disconnect players + turn off the server"""

		print("Initialising server")
		self.stage1()
		print("Server initialised")

		print("Drawing starting tiles and sending them to players")
		self.stage2()
		print("All starting racks sent")

		#print("Proper game starts!")
		self.stage3()
		#print("We have a winner")

		print("Closing server")
		self.stage4()

		return

	def stage1(self):
		"""Initialise server and wait for players to join"""
		self.server.start()	# wait for all players to join
		self.server.send_all(Message(MessageType.GAME_STARTS, "Starting game"))

	def stage2(self):
		"""Initialise game: create tile rack for all players and send them their initial tiles"""
		for client_id in self.server.clients.keys():
			self.racks[client_id] = Rack()

			for i in range(14):
				self.racks[client_id].add_tile(self.tile_pool.draw_random_tile())

			self.server.send(client_id, Message(MessageType.TRUE_RACK, self.racks[client_id]))

	def stage3(self):
		"""Proper game loop. Players take turns and perform actions"""
		pass

	def stage4(self):
		"""End game, disconnect players, turn off the server"""
		self.server.close()
		pass
