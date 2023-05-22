import socket
import msvcrt
import pickle
from typing import Optional

from .message import Message, MessageType
from .server_info_aggregator import ServerInfoAggregator


def get_server_ip():
    """
        Returns local IP.
    """
    return socket.gethostbyname(socket.gethostname())


class Server:
    def __init__(self, port):

        self.s = None
        self.ip = get_server_ip()

        self.port = port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.s.bind((self.ip, self.port))  # TCP server has started
        self.s.setblocking(False)  # Waiting for players does not block the server
        self.s.listen()  # TCP server is now listening

        self.clients: ServerInfoAggregator = ServerInfoAggregator()
        self.clients_count = 0

    def check_for_incoming_connections(self):
        try:
            # accept a new connection
            client_socket, client_address = self.s.accept()
            return self.__handle_new_client(client_socket, client_address)

        except IOError as e:
            # handle the case where there are no incoming connections
            pass

    def __handle_new_client(self, client_socket, client_address):

        # Receive client's username
        client_socket.settimeout(5)
        # client_socket.recv(1024).decode()
        message = pickle.loads(client_socket.recv(1024))
        print(message)
        client_username = message.content
        client_socket.settimeout(None)

        # add client to the dictionary
        assigned_client_id = self.clients.add_client(client_socket, client_address, client_username)
        self.clients_count += 1

        # send client assigned id
        self.send(assigned_client_id, Message(MessageType.PLAYER_JOINED, assigned_client_id))

        # return new client credentials
        return client_username, client_address, assigned_client_id

    def close(self):
        """Closes all connections and socket itself"""

        for client_id in self.clients.get_client_ids():
            self.clients.get_socket(client_id).close()
        if self.s:
            self.s.close()

        print("Closed all connections and socket")

    def send(self, client_id, message: Message):
        self.clients.get_socket(client_id).sendall(pickle.dumps(message))

    def send_all(self, message: Message):
        for client_id in self.clients.get_client_ids():
            self.send(client_id, message)

    def send_all_except(self, exempted_client_id, message: Message):
        """Sends message to all connected clients except for the exempted one."""

        for client_id in self.clients.get_client_ids():
            if client_id != exempted_client_id:
                self.send(client_id, message)

    def receive(self, client_id, blocking: bool) -> Optional[Message]:
        """Receives message from client with the given id.
        Returns string"""
        self.clients.get_socket(client_id).setblocking(blocking)

        try:
            received_msg = self.clients.get_socket(client_id).recv(2048)
            if received_msg:
                message = pickle.loads(received_msg)
                print(message)
                return message
            else:
                return None
        except IOError as e:
            # handle the case where there are no incoming messages
            pass

    def get_clients_count(self):
        """Returns number of connected clients."""
        return self.clients_count
