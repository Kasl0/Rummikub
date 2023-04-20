import socket


class Client:
    def __init__(self):
        self.username = input("Enter your username: ")
        self.ip = input("Enter the server IP: ")
        self.port = int(input("Enter the server port: "))

    def send(self, message):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            s.sendall(message.encode())
