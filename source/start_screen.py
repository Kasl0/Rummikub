from client import Client
from server_game import ServerGame


class StartScreen:
    def __init__(self):
        while True:
            print("Rummikub")
            print("1. Join game")
            print("2. Host game")
            print("3. Exit")

            choice = input("Select option (enter \"1\", \"2\" or \"3\"): ")

            if choice == "1":

                # Client - joining a session
                client = Client()
                client.connect()
                print("Server:", client.receive())  # Client waits for starting game signal

                # Client - game initialization

                for i in range(14):  # receive 14 tiles
                    print("Tile from the server:", client.receive())
                    # TODO: Parse received string to Tile object and add tile to player's rack

                print("All tiles received")

                # Client - actual game
                #
                #
                #
                #

                client.close_connection()
                break

            elif choice == "2":

                ServerGame().play()

                break

            elif choice == "3":
                break

            else:
                print("Invalid option selection")
