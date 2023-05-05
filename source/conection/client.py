import pickle
import socket

from .message import Message, MessageType


class Client:
    def __init__(self, username, ip, port):

        # client's socket
        self.s = None

        # client's id (for socket communication)
        self.id = None

        # client's username
        self.username = username
        # self.username = "Jan"

        # server's ip
        self.ip = ip
        # self.ip = "192.168.0.228"

        # server's port
        self.port = port
        # self.port = 1234

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

        self.s.setblocking(False)  # Socket does not block the client app

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
        try:

            if self.s and self.s.fileno() != -1:
                received_msg = self.s.recv(1024)
                if received_msg:
                    message = pickle.loads(received_msg)
                    print(message)
                    return message
                else:
                    return None
            else:
                print("Not connected to server.")

        except IOError as e:
            # handle the case where there are no incoming messages
            pass
