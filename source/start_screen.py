from client import Client
from server import Server
from tile_pool import TilePool


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

                # Server - session creation
                server = Server()
                server.start()

                # Server - game initialization
                tile_pool = TilePool()

                for client_id in server.clients.keys():

                    # draw 14 tiles
                    for i in range(14):
                        server.send(client_id, str(tile_pool.draw_random_tile()))

                print("All tiles dealt")

                # Server - actual game
                #
                #
                #
                #

                server.close()
                break

            elif choice == "3":
                break

            else:
                print("Invalid option selection")
