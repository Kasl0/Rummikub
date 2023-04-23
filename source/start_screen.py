from client import Client
from server_game import ServerGame
from client_game import ClientGame
import pickle

from board import Board
from message import MessageType


class StartScreen:
    def __init__(self):
        while True:
            print("Rummikub")
            print("1. Join game")
            print("2. Host game")
            print("3. For testing purposes only")
            print("4. Exit")

            choice = input("Select option (enter '1', '2', '3' or '4'): ")

            if choice == "1":
                ClientGame().play()
                break

            elif choice == "2":
                ServerGame().play()
                break

            elif choice == "3":
                print(MessageType.JOIN)
                break

            elif choice == "4":
                break
            else:
                print("Invalid option selection")
