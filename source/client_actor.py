from board import Board
from rack import Rack
from client import Client
from message import MessageType, Message
from board_change import BoardChange, BoardChangeType
from input_parser import InputParser
from tile import Tile
from vector2d import Vector2d
from enum import Enum


class ClientActorState(Enum):
    ACTIVE = 1,
    PASSIVE = 2


class ClientActor:
    """Represents the player

    Interacts with his board and has his rack.
    Communicate with Server through Client.

    """
    def __init__(self, board: Board, rack: Rack, client: Client):
        self.board = board
        self.rack = rack
        self.client = client
        self.state = ClientActorState.PASSIVE

    def play_main_game_part(self):
        """ Main game loop. If your turn, perform actions, else listen to changes"""
        while True:
            print("Enter passive state")
            while self.state == ClientActorState.PASSIVE:    # here we receive messages and react adequately
                print()
                print(self.rack)
                print(self.board)
                message = self.client.receive()

                if message.type == MessageType.CHANGE_INTRODUCED:
                    self.handle_board_change(message.content)

                elif message.type == MessageType.TRUE_BOARD:
                    self.board = message.content

                elif message.type == MessageType.NEXT_TURN:
                    if int(message.content) == self.client.id:
                        self.state = ClientActorState.ACTIVE
                        break

                elif message.type == MessageType.GAME_ENDS:
                    return message.content

                else:
                    raise ValueError("Received unexpected message: " + message.__str__())

            print("Enter active state")
            while self.state == ClientActorState.ACTIVE:
                print()
                print(self.rack)
                print(self.board)

                #   TODO: For now we choose action from console
                print("Choose your action:\n"
                      "\tdraw\n"
                      "\tplace <position_x> <position_y> <value> <color>\n"
                      "\tmove <position_from_x> <position_from_y> <position_to_x> <position_to_y>\n"
                      "\tremove <position_x> <position_y>\n"
                      "\trevert\n"
                      "\tconfirm\n"
                      "> ")
                parser = InputParser()
                if parser.is_draw():    # MessageType.DRAW_TILE
                    self.handle_draw_tile()
                    break

                elif parser.is_place():    # MessageType.CHANGE_INTRODUCED
                    self.handle_board_change_place(Tile(parser.get_value(), parser.get_color()), parser.get_position())
                elif parser.is_move():      # MessageType.CHANGE_INTRODUCED
                    self.handle_board_change_move(parser.get_position(), parser.get_position2())
                elif parser.is_remove():    # MessageType.CHANGE_INTRODUCED
                    self.handle_board_change_remove(parser.get_position())

                elif parser.is_revert():  # MessageType.REVERT_CHANGES:
                    self.handle_revert_changes()
                elif parser.is_confirm():  # MessageType.CONFIRM_CHANGES:
                    response = self.handle_confirm_changes()
                    if response[0]:
                        self.state = ClientActorState.PASSIVE
                        break
                    else:
                        print("Board not correct: " + response.__str__())
                else:
                    print("Received unexpected action: " + parser.words.__str__())

            # wait for NEXT_TURN
            message = self.client.receive()

            # change your state accordingly
            if message.type == MessageType.NEXT_TURN:
                if int(message.content) == self.client.id:
                    self.state = ClientActorState.ACTIVE
                else:
                    self.state = ClientActorState.PASSIVE
            else:
                raise ValueError("Received unexpected message: " + message.__str__())

    #######################
    ### ACTION HANDLERS ###
    #######################

    def handle_board_change(self, board_change: BoardChange):
        if board_change.change_type == BoardChangeType.PLACE:
            self.place_tile(board_change.tile, board_change.first_position, remove_from_rack=False)

        elif board_change.change_type == BoardChangeType.MOVE:
            self.board.move_tile(board_change.first_position, board_change.second_position)

        elif board_change.change_type == BoardChangeType.REMOVE:
            self.take_tile_off_board(board_change.first_position, add_to_rack=False)

        else:
            raise ValueError("Received unexpected board change type: " + board_change.change_type.__str__())

    def handle_draw_tile(self):
        """Ask server for a tile and add it to the rack"""
        self.client.send(Message(MessageType.DRAW_TILE, None))
        self.receive_true_board_and_rack()

    def handle_board_change_place(self, tile: Tile, position: Vector2d):
        if self.rack.if_tile_on_rack(tile):
            # introduce change on your own board and rack
            self.place_tile(tile, position, remove_from_rack=True)

            # prepare change for server
            board_change = BoardChange(BoardChangeType.PLACE, tile, position, None)
            self.client.send(Message(MessageType.CHANGE_INTRODUCED, board_change))

        else:
            print("Failed to place tile: " + tile.__str__() + ", player doesn't have on their rack")

    def handle_board_change_move(self, position1: Vector2d, position2: Vector2d):
        # introduce change on your own board
        self.board.move_tile(position1, position2)

        # prepare change for server
        board_change = BoardChange(BoardChangeType.MOVE, None, position1, position2)
        self.client.send(Message(MessageType.CHANGE_INTRODUCED, board_change))

    def handle_board_change_remove(self, position: Vector2d):
        # introduce change on your own board and rack
        self.take_tile_off_board(position, add_to_rack=True)

        # prepare change for server
        board_change = BoardChange(BoardChangeType.REMOVE, None, position, None)

        self.client.send(Message(MessageType.CHANGE_INTRODUCED, board_change))

    def handle_revert_changes(self):
        self.client.send(Message(MessageType.REVERT_CHANGES, None))
        self.receive_true_board_and_rack()

    def handle_confirm_changes(self):
        self.client.send(Message(MessageType.CONFIRM_CHANGES, None))
        message = self.client.receive()

        if message.type.OK or message.type.NOT_OK:
            return message.content
        else:
            raise ValueError("Received unexpected message: " + message.__str__())

    #########################
    ### AUXILIARY METHODS ###
    #########################

    def receive_true_board_and_rack(self):
        for _ in range(2):  # we will receive true board AND true rack
            message = self.client.receive()
            if message.type == MessageType.TRUE_BOARD:
                self.board = message.content
            elif message.type == MessageType.TRUE_RACK:
                self.rack = message.content
            else:
                raise ValueError("Received unexpected message: " + message.__str__())

    ############################################
    ### FOR INTERACTIONS WITH BOARD AND RACK ###
    ############################################

    def place_tile(self, tile: Tile, position: Vector2d, remove_from_rack: bool):
        """Place given tile on given position at the board"""
        if remove_from_rack:
            self.rack.remove_tile(tile)

        self.board.place_tile(tile, position)

    def take_tile_off_board(self, position: Vector2d, add_to_rack: bool):
        """Take tile off the board and add it to player's rack"""

        tile = self.board.take_tile_off(position)
        if tile is not None and add_to_rack:
            self.rack.add_tile(tile)
