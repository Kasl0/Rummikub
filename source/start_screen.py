from client import Client
from server import Server


class StartScreen:
    def __init__(self):
        while True:
            print("Rummikub")
            print("1. Join game")
            print("2. Host game")
            print("3. Exit")

            choice = input("Select option (enter \"1\", \"2\" or \"3\"): ")

            if choice == "1":
                client = Client()
                client.send(client.username)  # client sends his username to the server
                break
            elif choice == "2":
                server = Server()
                server.start()
                break
            elif choice == "3":
                break
            else:
                print("Invalid option selection")
