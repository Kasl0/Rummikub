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

    Interacts board and has his own rack.
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
            while self.state == ClientActorState.PASSIVE:    # here we receive messages and react adequately
                message = self.client.receive()

                if message.type == MessageType.CHANGE_INTRODUCED:
                    self.introduce_board_change(message.content)

                elif message.type == MessageType.TRUE_BOARD:
                    self.board = message.content

                elif message.type == MessageType.NEXT_TURN:
                    if message.content == self.client.id:
                        self.state = ClientActorState.ACTIVE
                        break

                elif message.type == MessageType.GAME_ENDS:
                    print("And the winner is... " + message.content + "!")
                    return  # catapult out of this whole function

                else:
                    raise ValueError("Received unexpected message: " + message.__str__())

            while self.state == ClientActorState.ACTIVE:
                #   TODO: Right now we choose action from console
                parser = InputParser()
                if parser.is_draw():    # MessageType.DRAW_TILE
                    self.draw_tile()
                elif parser.is_place() or parser.is_move() or parser.is_remove():   # MessageType.CHANGE_INTRODUCED
                    board_change = None

                    if parser.is_place():
                        tile = Tile(parser.get_value(), parser.get_color())
                        position = parser.get_position()

                        # introduce change on your own board and rack
                        self.place_tile(tile, position, remove_from_rack=True)
                        print(self.rack)
                        print(self.board)

                        # prepare change for server
                        board_change = BoardChange(BoardChangeType.PLACE, tile, position, None)

                    elif parser.is_move():
                        position1 = parser.get_position()
                        position2 = parser.get_position2()

                        # introduce change on your own board
                        self.board.move_tile(position1, position2)
                        print(self.rack)
                        print(self.board)

                        # prepare change for server
                        board_change = BoardChange(BoardChangeType.MOVE, None, position1, position2)

                    elif parser.is_remove():
                        position = parser.get_position()

                        # introduce change on your own board and rack
                        self.take_tile_off_board(position, add_to_rack=True)
                        print(self.rack)
                        print(self.board)

                        # prepare change for server
                        board_change = BoardChange(BoardChangeType.REMOVE, None, position, None)

                    self.client.send(Message(MessageType.CHANGE_INTRODUCED, board_change))

                elif parser == MessageType.REVERT_CHANGES:
                    self.revert_changes()
                elif parser == MessageType.CONFIRM_CHANGES:
                    if self.try_to_confirm_changes():
                        self.state = ClientActorState.PASSIVE
                else:
                    print("Received unexpected action: " + parser.__str__())

    ####################################
    ### FOR INTERACTIONS WITH CLIENT ###
    ####################################

    def introduce_board_change(self, board_change: BoardChange):
        if board_change.change_type == BoardChangeType.PLACE:
            self.place_tile(board_change.tile, board_change.first_position, False)

        elif board_change.change_type == BoardChangeType.MOVE:
            self.board.move_tile(board_change.first_position, board_change.second_position)

        elif board_change.change_type == BoardChangeType.REMOVE:
            self.take_tile_off_board(board_change.first_position, False)

        else:
            raise ValueError("Received unexpected board change type: " + board_change.change_type.__str__())

    def draw_tile(self):
        """Ask server for a tile and add it to the rack"""
        self.client.send(Message(MessageType.DRAW_TILE, None))
        message = self.client.receive()

        if message.type == MessageType.TILE:
            self.rack.add_tile(message.content)
        else:
            raise ValueError("Received unexpected message: " + message.__str__())

    def revert_changes(self):
        self.client.send(Message(MessageType.REVERT_CHANGES, None))
        message = self.client.receive()

        for i in range(2):  # we will receive true board AND true rack
            if message.type == MessageType.TRUE_BOARD:
                self.board = message.content
            elif message.type == MessageType.TRUE_RACK:
                self.rack = message.content
            else:
                raise ValueError("Received unexpected message: " + message.__str__())

    def try_to_confirm_changes(self):
        self.client.send(Message(MessageType.CONFIRM_CHANGES, None))
        message = self.client.receive()

        if message.type.OK:
            return True
        elif message.type.NOT_OK:
            return False
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
