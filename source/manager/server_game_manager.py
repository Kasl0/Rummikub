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

	def session_initialization(self):
		self.server.send_all(Message(MessageType.GAME_STARTS, "Starting game"))

	def game_initialization(self):
		for client_id in self.server.clients.get_client_ids():
			self.racks[client_id] = Rack()

			for i in range(14):
				self.racks[client_id].add_tile(self.tile_pool.draw_random_tile())

			self.server.send(client_id, Message(MessageType.TRUE_RACK, self.racks[client_id]))
		self.server_actor.start_next_turn()

	def update_main_game(self):
		return self.server_actor.update_main_game()

	def game_has_ended(self):
		return self.server_actor.game_has_ended()

