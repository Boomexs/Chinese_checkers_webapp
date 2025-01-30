import copy

from board import Board
from moveValidator import MoveValidator, GameStrategy
import random

class Bot:
    def __init__(self, player: int, game_strategy: GameStrategy):
        self.player = player
        self.move_validator = MoveValidator(game_strategy)
        self.destination_index = None

    def make_move(self, board: Board):
        pieces = self._find_your_pieces(board)
        self._set_your_destination_index(board)
        best_move = self._find_the_best_move(pieces, board)
        return best_move

    def _find_your_pieces(self, board: Board):
        nodes = board.board_to_full_data()
        pieces = []
        for row in nodes:
            for node in row:
                if node['content'] == self.player:
                    pieces.append(node)
        return pieces

    def _set_your_destination_index(self, board: Board):
        zones = board.zones
        zones_dir = {"up": "down", "down": "up", "left_up": "right_down", "left_down": "right_up", "right_up": "left_down", "right_down": "left_up"}
        destinations_index_dir = {"up": 0, "down": 120, "left_up": 10, "left_down": 98, "right_up": 22, "right_down": 110}
        for zone_name, zone_nodes in zones.items():
            if zone_nodes and zone_nodes[0].content == self.player:
                destination_zone = zones_dir[zone_name]
                self.destination_index = destinations_index_dir[destination_zone]
                break

    @staticmethod
    def _convert_moves_to_indexes(board_data):
        indexes = []
        flat_index = 0  # Track the flat index across the entire board

        for row in board_data:
            for cell in row:
                if cell is not None:  # Skip None or invalid cells
                    if cell == -2:  # Check if the cell represents a valid move
                        indexes.append(flat_index)
                    flat_index += 1  # Increment the flat index only for valid cells

        return indexes

    def _evaluate_move(self, piece_id , move_id: int):
        return abs(self.destination_index - move_id) / ( abs(self.destination_index - piece_id) * abs(piece_id - move_id))

    def _find_the_best_move(self, pieces: list, board: Board):
        best_move = None
        best_mov_eval = float('inf')

        copy_board = copy.deepcopy(board)
        while True:
            piece = random.choice(pieces)
            moves = self._convert_moves_to_indexes(self.move_validator.possible_moves(board, piece['id'], self.player))
            if moves:
                print('Moves:', moves)
                for move in moves:
                    move_eval = self._evaluate_move(piece['id'], move)
                    if move_eval <= best_mov_eval:
                        best_move = move
                        best_mov_eval = move_eval
                break
                moves.clear()
        return best_move