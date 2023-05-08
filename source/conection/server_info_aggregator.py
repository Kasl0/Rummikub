from random import choice
from socket import socket
from typing import Dict, Tuple


class ServerInfoAggregator:
	# dictionary of clients
	# keys - assigned client ids
	# values - tuple of 3 elements: client_socket, client_address, client_username

	def __init__(self):
		self._clients: Dict[int, Tuple[socket, any, str]] = {}

		# clients are assigned ids from 1 up to n, so every number from interval <1, n> has associated client
		self.next_free_id = 1

	def add_client(self, client_socket: socket, client_address: any, client_username: str):
		self._clients[self.next_free_id] = (client_socket, client_address, client_username)
		self.next_free_id += 1
		return self.next_free_id - 1

	def get_client_ids(self):
		return self._clients.keys()

	def get_socket(self, client_id: int):
		return self._get_nth_element_of_client(client_id, 0)

	def get_address(self, client_id: int):
		return self._get_nth_element_of_client(client_id, 1)

	def get_username(self, client_id: int):
		return self._get_nth_element_of_client(client_id, 2)

	def _get_nth_element_of_client(self, client_id: int, n: int):
		searched_client = self._clients[client_id]
		if searched_client is None:
			return None
		return searched_client[n]

	def get_next_client_id(self, client_id: int):
		return client_id + 1 if client_id + 1 <= len(self._clients) else 1

	def get_random_client_id(self):
		return choice(list(self._clients.keys()))




