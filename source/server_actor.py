from copy import deepcopy
from time import sleep
from typing import Dict

from board import Board
from rack import Rack
from message import MessageType, Message
from board_change import BoardChange, BoardChangeType
from server import Server
from tile_pool import TilePool
from tile import Tile
from vector2d import Vector2d


class ServerActor:
    """Represents the server

    Manages whole game session. Informs players about next turns. Listens to active player.
    It synchronises changes introduced by an active player and informs passive players about them.
    Has one, true and only valid board and racks states.
    """

    def __init__(self, racks: Dict[int, Rack], tile_pool: TilePool, server: Server):
        self.true_board = Board()
        self.temp_board = Board()

        self.temp_rack = Rack()
        self.true_racks = racks

        self.tile_pool = tile_pool

        self.server = server

        self.active_player_id = 1

    def serve_main_game_part(self) -> int:
        """ Main game loop. If your turn, perform actions, else listen to changes"""
        while True:
            print("New turn starts. Active player: " + self.active_player_id.__str__())
            self.temp_board = deepcopy(self.true_board)
            self.temp_rack = deepcopy(self.true_racks[self.active_player_id])

            self.announce_next_turn()

            while True:
                print()
                print(self.temp_rack)
                print(self.temp_board)
                message = self.server.receive(self.active_player_id)

                if message.type == MessageType.DRAW_TILE:
                    self.server.send_all(Message(MessageType.TRUE_BOARD, self.true_board))

                    drawn_tile = self.tile_pool.draw_random_tile()
                    self.true_racks[self.active_player_id].add_tile(drawn_tile)
                    self.server.send(self.active_player_id, Message(MessageType.TRUE_RACK, self.true_racks[self.active_player_id]))
                    break

                elif message.type == MessageType.CHANGE_INTRODUCED:
                    self.introduced_board_change(message.content)

                elif message.type == MessageType.REVERT_CHANGES:
                    self.temp_board = deepcopy(self.true_board)
                    self.temp_rack = deepcopy(self.true_racks[self.active_player_id])

                    self.server.send_all(Message(MessageType.TRUE_BOARD, self.true_board))
                    # TODO: Will sleep be necessary here? Won't these two messages collide at active player's client?
                    self.server.send(self.active_player_id, Message(MessageType.TRUE_RACK, self.true_racks[self.active_player_id]))

                elif message.type == MessageType.CONFIRM_CHANGES:
                    verification_result = self.temp_board.verify()

                    if verification_result[0]:
                        self.server.send(self.active_player_id, Message(MessageType.OK, verification_result))
                        self.persist_temporary_elements()
                        self.server.send_all_except(
                            self.active_player_id,
                            Message(MessageType.TRUE_BOARD, self.true_board))
                        break
                    else:
                        self.server.send(self.active_player_id, Message(MessageType.NOT_OK, verification_result))

                else:
                    raise ValueError("Received unexpected message: " + message.__str__())

            # if game should end
            if self.temp_rack.is_empty():
                return self.active_player_id

            if self.active_player_id + 1 <= len(self.server.clients):
                self.active_player_id = self.active_player_id + 1
            else:
                self.active_player_id = 1

    ####################################
    ### FOR INTERACTIONS WITH CLIENT ###
    ####################################

    def introduced_board_change(self, board_change: BoardChange):
        if board_change.change_type == BoardChangeType.PLACE:
            self.place_tile(board_change.tile, board_change.first_position)

        elif board_change.change_type == BoardChangeType.MOVE:
            self.temp_board.move_tile(board_change.first_position, board_change.second_position)

        elif board_change.change_type == BoardChangeType.REMOVE:
            self.take_tile_off_board(board_change.first_position)

        else:
            raise ValueError("Received unexpected board change type: " + board_change.change_type.__str__())

        self.server.send_all_except(self.active_player_id, Message(MessageType.CHANGE_INTRODUCED, board_change))

    def announce_next_turn(self):
        # TODO: Not very professional, but otherwise active player won't get NEXT_TURN message
        sleep(1)
        self.server.send_all(Message(MessageType.NEXT_TURN, self.active_player_id))

    ######################################################
    ### FOR INTERACTIONS WITH temporary BOARD AND RACK ###
    ######################################################

    def persist_temporary_elements(self):
        self.true_board = self.temp_board
        self.true_racks[self.active_player_id] = self.temp_rack

    def place_tile(self, tile: Tile, position: Vector2d):
        """Place given tile on given position at the temporary board"""
        self.temp_rack.remove_tile(tile)
        self.temp_board.place_tile(tile, position)

    def take_tile_off_board(self, position: Vector2d):
        """Take tile off the temporary board and add it to the temporary rack"""

        tile = self.temp_board.take_tile_off(position)
        if tile is not None:
            self.temp_rack.add_tile(tile)
