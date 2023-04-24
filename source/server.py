import socket
import msvcrt
import random
import pickle

from message import Message, MessageType


class Server:
    def __init__(self):

        self.s = None
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)

        print("Server IP:", self.ip)
        self.port = 1234
        # TODO: revert input
        #self.port = int(input("Enter the server port: "))

        # dictionary of clients
        # keys - assigned client ids
        # values - arrays of 3 elements: client_socket, client_address, client_username
        self.clients = {}

        self.next_free_id = 1

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.s.bind((self.ip, self.port))  # TCP server has started
        self.s.setblocking(False)  # Waiting for players does not block the server
        self.s.listen()  # TCP server is now listening

    def start(self):
        """Waits for the players and calls self.__init_game()
        when there was an action to start the game"""

        print("Game lobby is now open - waiting for players")

        # wait for incoming connections
        while True:

            # TODO: Make "Start game" button and check if it is pressed in bellow's if statement
            #  Temporary solution: Game is started when user presses any key
            #  Works only in cmd outside PyCharm!!!
            #  In PyCharm msvcrt.kbhit() doesn't detect key press and you can't start a game by any means
            if msvcrt.kbhit():
                break
            else:
                try:
                    # accept a new connection
                    client_socket, client_address = self.s.accept()
                    self.__handle_new_client(client_socket, client_address)

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
        self.clients[self.next_free_id] = [client_socket, client_address, client_username]

        # print new client credentials
        print("New player:", client_username, client_address, "with assigned ID:", self.next_free_id)

        # send client assigned id
        self.send(self.next_free_id, Message(MessageType.PLAYER_JOINED, self.next_free_id))

        self.next_free_id += 1

    def close(self):
        """Closes all connections and socket itself"""

        for client_id in self.clients.keys():
            self.clients[client_id][0].close()
        if self.s:
            self.s.close()

        print("Closed all connections and socket")

    def send(self, client_id, message: Message):
        """Sends message to the client by the given id."""

        self.clients[client_id][0].sendall(pickle.dumps(message))

    def send_all(self, message: Message):
        """Sends message to all connected clients."""

        for client_id in self.clients.keys():
            self.send(client_id, message)

    def send_all_except(self, exempted_client_id, message: Message):
        """Sends message to all connected clients except for the exempted one."""

        for client_id in self.clients.keys():
            if client_id != exempted_client_id:
                self.send(client_id, message)

    def receive(self, client_id) -> Message:
        """Receives message from client with the given id.
        Returns string"""

        message = pickle.loads(self.clients[client_id][0].recv(1024))
        print(message)
        return message

    def get_random_client_id(self):
        """Returns id of random client"""

        return random.choice(list(self.clients.keys()))
