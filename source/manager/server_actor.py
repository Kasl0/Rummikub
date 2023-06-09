from copy import deepcopy
from time import sleep
from typing import Dict, Optional

from ..logic.board import Board
from ..logic.rack import Rack
from ..conection.message import MessageType, Message
from ..conection.board_change import BoardChange, BoardChangeType
from ..conection.server import Server
from ..logic.tile_pool import TilePool
from ..logic.tile import Tile, Color
from ..logic.vector2d import Vector2d


class ServerActor:
    """Represents the main game part master

    Manages game main part. Informs players about next turns. Listens to active player.
    Synchronises changes introduced by an active player and informs passive players about them.
    Has one, true and only valid board and racks states."""

    def __init__(self, racks: Dict[int, Rack], tile_pool: TilePool, server: Server):
        self.true_board = Board()
        self.__temp_board = Board()

        self.__temp_rack = Rack()
        # starting temp rack cannot be empty, otherwise the game will end immediately
        self.__temp_rack.add_tile(Tile(Tile.Joker, Color.Joker))
        self.__true_racks = racks

        self.tile_pool = tile_pool

        self.server = server

        self.active_player_id = 1

    def start_next_turn(self):
        # if game should end
        if self.__temp_rack.is_empty():
            return self.__end_main_game(self.active_player_id)

        # get next player
        self.active_player_id = self.server.clients.get_next_client_id(self.active_player_id)

        print("New turn starts. Active player: " + self.active_player_id.__str__())
        self.__temp_board = deepcopy(self.true_board)
        self.__temp_rack = deepcopy(self.__true_racks[self.active_player_id])

        self.__announce_next_turn()

    def update_main_game(self) -> Optional[Message]:
        """Check if there are any waiting Messages to handle"""
        message = self.server.receive(self.active_player_id, blocking=False)

        if message is None:
            return None

        if message.type == MessageType.DRAW_TILE:
            self.__handle_draw_tile()
            self.start_next_turn()

        elif message.type == MessageType.CHANGE_INTRODUCED:
            self.__handle_introduced_change(message.content)

        elif message.type == MessageType.REVERT_CHANGES:
            self.__handle_revert_changes()

        elif message.type == MessageType.CONFIRM_CHANGES:
            result = self.__handle_confirm_changes()
            print("Confirmation response: " + result.__str__())
            if result[0]:
                self.start_next_turn()
        else:
            raise ValueError("Received unexpected message: " + message.__str__())

        return message

    #################################
    # ACTIVE PLAYER ACTION HANDLERS #
    #################################

    def __handle_draw_tile(self):
        self.server.send_all(Message(MessageType.TRUE_BOARD, self.true_board))
        drawn_tile = self.tile_pool.draw_random_tile()
        if drawn_tile:
            self.__true_racks[self.active_player_id].add_tile(drawn_tile)
        self.server.send(self.active_player_id, Message(MessageType.TRUE_RACK, self.__true_racks[self.active_player_id]))

    def __handle_introduced_change(self, board_change: BoardChange):
        if board_change.change_type == BoardChangeType.PLACE:
            self.__place_tile_on_temporary_board(board_change.tile, board_change.first_position)

        elif board_change.change_type == BoardChangeType.MOVE:
            self.__temp_board.move_tile(board_change.first_position, board_change.second_position)

        elif board_change.change_type == BoardChangeType.REMOVE:
            self.__take_tile_off_temporary_board(board_change.first_position)

        else:
            raise ValueError("Received unexpected board change type: " + board_change.change_type.__str__())

        self.server.send_all_except(self.active_player_id, Message(MessageType.CHANGE_INTRODUCED, board_change))

    def __handle_revert_changes(self):
        self.__temp_board = deepcopy(self.true_board)
        self.__temp_rack = deepcopy(self.__true_racks[self.active_player_id])
        self.server.send_all(Message(MessageType.TRUE_BOARD, self.true_board))
        self.server.send(self.active_player_id, Message(MessageType.TRUE_RACK, self.__true_racks[self.active_player_id]))

    def __handle_confirm_changes(self):
        def confirmation_approved():
            self.server.send(self.active_player_id, Message(MessageType.OK, verification_result))
            self.__persist_temporary_elements()
            self.server.send_all_except(
                self.active_player_id,
                Message(MessageType.TRUE_BOARD, self.true_board))

        def confirmation_rejected():
            self.server.send(self.active_player_id, Message(MessageType.NOT_OK, verification_result))

        verification_result = self.__temp_board.verify()
        if verification_result[0]:
            confirmation_approved()
        else:
            confirmation_rejected()
        return verification_result

    #####################
    # AUXILIARY METHODS #
    #####################

    def __announce_next_turn(self):
        # TODO: Not very professional, but otherwise active player won't get NEXT_TURN message
        #  and I have no idea why it's like that. I even created separate method __receive_board_and_rack_and_next_turn
        #  in ClientActor but to no avail
        sleep(1)
        message_content = (self.active_player_id, self.server.clients.get_username(self.active_player_id))
        self.server.send_all(Message(MessageType.NEXT_TURN, message_content))

    def __persist_temporary_elements(self):
        self.true_board = self.__temp_board
        self.__true_racks[self.active_player_id] = self.__temp_rack

    # TODO: test game ending sequence
    def __end_main_game(self, client_id: int):
        winner_username = self.server.clients.get_username(client_id)
        self.server.send_all(Message(MessageType.GAME_ENDS, winner_username))
        self.server.close()
        return winner_username

    ##################################################
    # FOR INTERACTIONS WITH temporary BOARD AND RACK #
    ##################################################

    def __place_tile_on_temporary_board(self, tile: Tile, position: Vector2d):
        """Place given tile on given position at the temporary board"""
        self.__temp_rack.remove_tile(tile)
        self.__temp_board.place_tile(tile, position)

    def __take_tile_off_temporary_board(self, position: Vector2d):
        """Take tile off the temporary board and add it to the temporary rack"""

        tile = self.__temp_board.take_tile_off(position)
        if tile is not None:
            self.__temp_rack.add_tile(tile)
