from ..manager.client_game_manager import ClientGameManager
from ..manager.server_game_manager import ServerGameManager


class StartScreen:
    def __init__(self):
        while True:
            print("Rummikub")
            print("1. Join game")
            print("2. Host game")
            print("3. For testing purposes only")
            print("4. Exit")

            choice = input("Select option (enter '1', '2' or '3')\n> ")

            if choice == "1":
                ClientGameManager().play()
                break

            elif choice == "2":
                ServerGameManager().play()
                break

            elif choice == "4":
                break
            else:
                print("Invalid option selection")
