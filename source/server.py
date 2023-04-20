import os
import socket


class Server:
    def __init__(self):

        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)

        print("Server IP: " + self.ip)
        self.port = int(input("Enter the server port: "))

    def start(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.bind((self.ip, self.port))  # TCP server has started
            s.setblocking(False)  # Waiting for players does not block the server
            s.listen()  # TCP server is now listening

            print("Game lobby is now open")

            # wait for incoming connections
            while True:
                try:
                    # accept a new connection
                    client_socket, client_address = s.accept()

                    # print the client address
                    print("Client address:", client_address)
                    data = client_socket.recv(1024)
                    print('Received message: ', data.decode())

                    # close the client socket
                    client_socket.close()

                except IOError as e:
                    # handle the case where there are no incoming connections
                    pass
