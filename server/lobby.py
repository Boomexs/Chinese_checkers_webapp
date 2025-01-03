from board import Board
from board import Board

class Lobby:
    def __init__(self, lobby_name: str, needed_players: int):
        self.name = lobby_name
        self.players = []
        self.player_count = needed_players
        self.current_turn_index = 0
        self.board: Board = Board(needed_players)   # create a board object for x players; x=needed_players

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
