import pickle
import socket
from typing import Optional

from .message import Message, MessageType, MESSAGE_SIZE


class Client:
    def __init__(self, username, ip, port):

        # client's socket
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # client's id (for socket communication)
        self.id = None

        # client's username
        self._username = username

        # server's ip
        self._ip = ip

        # server's port
        self._port = port

    def connect(self, timeout=5):
        """
        Connects to the socket server, sends client's username,
        receives assigned client ID
        """
        self._s.settimeout(timeout)

        self._s.connect((self._ip, self._port))
        print("Connected with the server")

        self.send(Message(MessageType.JOIN, self._username))
        print("Username sent")

        self.id = int(self.receive(blocking=True).content)
        print("Assigned client ID: ", self.id)

    def close_connection(self):
        """Closes connection with the server"""
        if self._s:
            self._s.close()

        print("Closed connection with the server")

    def send(self, message: Message):
        """Sends message to the server."""

        if self._s and self._s.fileno() != -1:
            print("Sent:")
            print(message)
            self._s.sendall(pickle.dumps(message))
        else:
            print("Not connected to server.")

    def receive(self, blocking: bool) -> Optional[Message]:
        """Receives message from the server.

        :param blocking - tells if client should wait for next message indefinitely or
        if it should only peek if there is an awaiting message
        """
        self._s.setblocking(blocking)
        try:

            if self._s.fileno() != -1:
                received_msg = self._s.recv(MESSAGE_SIZE)
                if received_msg:
                    message = pickle.loads(received_msg)
                    print("Received:")
                    print(message)
                    return message
                else:
                    return None
            else:
                print("Not connected to server.")

        except IOError as e:
            # handle the case where there are no incoming messages
            pass
