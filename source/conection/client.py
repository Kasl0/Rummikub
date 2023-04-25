import pickle
import socket

from .message import Message, MessageType


class Client:
    def __init__(self):

        # client's socket
        self.s = None

        # client's id (for socket communication)
        self.id = None

        # client's username (entered by user)
        # self.username = "Jan"
        self.username = input("Enter your username: ")

        # server's ip (entered by user)
        # self.ip = "192.168.0.228"
        self.ip = input("Enter the server IP: ")

        # server's port (entered by user)
        # self.port = 1234
        self.port = int(input("Enter the server port: "))

    def connect(self):
        """Connects to the socket server, sends client's username,
        receives assigned client ID"""

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.ip, self.port))
        print("Connected with the server")

        self.send(Message(MessageType.JOIN, self.username))
        print("Username sent")

        self.id = int(self.receive().content)
        print("Assigned client ID: ", self.id)

    def close_connection(self):
        """Closes connection with the server"""
        if self.s:
            self.s.close()

        print("Closed connection with the server")

    def send(self, message: Message):
        """Sends message to the server."""

        if self.s and self.s.fileno() != -1:
            self.s.sendall(pickle.dumps(message))
        else:
            print("Not connected to server.")

    def receive(self) -> Message:
        """Receives message from the server."""

        if self.s and self.s.fileno() != -1:
            message = pickle.loads(self.s.recv(1024))
            print(message)
            return message
        else:
            print("Not connected to server.")
