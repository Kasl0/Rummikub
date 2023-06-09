from typing import Optional

from ..logic.board import Board
from ..logic.rack import Rack
from ..conection.client import Client
from ..conection.message import MessageType, Message
from ..conection.board_change import BoardChange, BoardChangeType
from ..logic.tile import Tile
from ..logic.vector2d import Vector2d
from enum import Enum


class ClientActorState(Enum):
    ACTIVE = 1,
    PASSIVE = 2


def assert_client_actor_has_state(client_state: ClientActorState):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if self.state != client_state:
                return
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


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
        self.winner_nickname: Optional[str] = None

        self.active_player_id: Optional[int] = None
        self.active_player_nick: str = ""

    @assert_client_actor_has_state(ClientActorState.PASSIVE)
    def check_if_should_introduce_changes(self) -> bool:
        # here we receive messages and react adequately
        message = self.client.receive(blocking=False)

        if not message:
            return False

        if message.type == MessageType.CHANGE_INTRODUCED:
            self.__handle_board_change(message.content)

        elif message.type == MessageType.TRUE_BOARD:
            self.board = message.content

        elif message.type == MessageType.NEXT_TURN:
            self.__handle_next_turn(message)

        elif message.type == MessageType.GAME_ENDS:
            self.winner_nickname = message.content

        else:
            raise ValueError("Received unexpected message: " + message.__str__())

        return True

    def check_if_game_should_end(self):
        return self.winner_nickname is not None

    ###################
    # ACTION HANDLERS #
    ###################

    def __handle_board_change(self, board_change: BoardChange):
        if board_change.change_type == BoardChangeType.PLACE:
            self.__place_tile(board_change.tile, board_change.first_position, remove_from_rack=False)

        elif board_change.change_type == BoardChangeType.MOVE:
            self.board.move_tile(board_change.first_position, board_change.second_position)

        elif board_change.change_type == BoardChangeType.REMOVE:
            self.__take_tile_off_board(board_change.first_position, add_to_rack=False)

        else:
            raise ValueError("Received unexpected board change type: " + board_change.change_type.__str__())

    @assert_client_actor_has_state(ClientActorState.ACTIVE)
    def handle_draw_tile(self):
        """Ask server for a tile and add it to the rack"""
        self.client.send(Message(MessageType.DRAW_TILE, None))
        self.__receive_board_and_rack()
        self.state = ClientActorState.PASSIVE

    @assert_client_actor_has_state(ClientActorState.ACTIVE)
    def handle_board_change_place(self, tile: Tile, position: Vector2d):
        if self.rack.if_tile_on_rack(tile):
            # introduce change on your own board and rack
            self.__place_tile(tile, position, remove_from_rack=True)

            # prepare change for server
            board_change = BoardChange(BoardChangeType.PLACE, tile, position, None)
            self.client.send(Message(MessageType.CHANGE_INTRODUCED, board_change))

        else:
            print("Failed to place tile: " + tile.__str__() + ", player doesn't have on their rack")

    @assert_client_actor_has_state(ClientActorState.ACTIVE)
    def handle_board_change_move(self, source_position: Vector2d, destined_position: Vector2d):
        # introduce change on your own board
        self.board.move_tile(source_position, destined_position)

        # prepare change for server
        board_change = BoardChange(BoardChangeType.MOVE, None, source_position, destined_position)
        self.client.send(Message(MessageType.CHANGE_INTRODUCED, board_change))

    @assert_client_actor_has_state(ClientActorState.ACTIVE)
    def handle_board_change_remove(self, position: Vector2d):
        # introduce change on your own board and rack
        self.__take_tile_off_board(position, add_to_rack=True)

        # prepare change for server
        board_change = BoardChange(BoardChangeType.REMOVE, None, position, None)

        self.client.send(Message(MessageType.CHANGE_INTRODUCED, board_change))

    @assert_client_actor_has_state(ClientActorState.ACTIVE)
    def handle_revert_changes(self):
        self.client.send(Message(MessageType.REVERT_CHANGES, None))
        self.__receive_board_and_rack()

    @assert_client_actor_has_state(ClientActorState.ACTIVE)
    def handle_confirm_changes(self):
        self.client.send(Message(MessageType.CONFIRM_CHANGES, None))
        message = self.client.receive(blocking=True)

        if message.type == MessageType.OK:
            self.state = ClientActorState.PASSIVE
        elif message.type == MessageType.NOT_OK:
            pass
        else:
            raise ValueError("Received unexpected message: " + message.__str__())

        return message.content

    def __handle_next_turn(self, message):
        active_player_id, self.active_player_nick = message.content
        self.state = ClientActorState.ACTIVE if active_player_id == self.client.id else ClientActorState.PASSIVE

    #####################
    # AUXILIARY METHODS #
    #####################

    def __receive_board_and_rack(self):
        for _ in range(2):  # we will receive true board and true rack
            message = self.client.receive(blocking=True)
            if message.type == MessageType.TRUE_BOARD:
                self.board = message.content
            elif message.type == MessageType.TRUE_RACK:
                self.rack = message.content
            else:
                raise ValueError("Received unexpected message: " + message.__str__())

    ########################################
    # FOR INTERACTIONS WITH BOARD AND RACK #
    ########################################

    def __place_tile(self, tile: Tile, position: Vector2d, remove_from_rack: bool):
        """Place given tile on given position at the board"""
        if remove_from_rack:
            self.rack.remove_tile(tile)

        self.board.place_tile(tile, position)

    def __take_tile_off_board(self, position: Vector2d, add_to_rack: bool):
        """Take tile off the board and add it to player's rack"""

        tile = self.board.take_tile_off(position)
        if tile is not None and add_to_rack:
            self.rack.add_tile(tile)
