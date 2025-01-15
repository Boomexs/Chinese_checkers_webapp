from board import Board
from board import Board

class Lobby:
    def __init__(self, lobby_name: str, needed_players: int):
        self.name = lobby_name
        self.players = []
        self.player_count = needed_players
        self.current_turn_index = 0
        self.board: Board = Board(needed_players)
        self.board.make_board()
        self.board.connect_board()
        # TEMP
        self.board.add_player('up',1)
        self.board.add_player('left_up',2)
        self.board.add_player('left_down',1)
        self.board.add_player('down',2)
        self.board.add_player('right_up',2)
        self.board.add_player('right_down',1)

    def add_player(self, player: str):
        if len(self.players) < self.player_count:
            self.players.append(player)
            return True
        return False

    def remove_player(self, player: str):
        self.players.remove(player)

    def is_full(self):
        return len(self.players) >= self.player_count

    def make_move(self, player: str, move: dict):
        if player != self.players[self.current_turn_index]:
            return {'success' : False, 'state' : 'Not your turn!'}
        return self.board.make_move(move)
