from board import Board
from board import Board

class Lobby:
    def __init__(self, lobby_name: str, needed_players: int):
        self.name = lobby_name
        self.players = []
        self.player_count = needed_players
        self.turn = 0
        self.board: Board = Board(needed_players)
        self.state: 'waiting'

    def add_player(self, player: str):
        if len(self.players) < self.player_count:
            self.players.append(player)
            return True
        return False

    def remove_player(self, player: str):
        self.players.remove(player)

    def is_full(self):
        return len(self.players) >= self.player_count

    def has_won(self):
        pass

    def next_turn(self):
        self.turn += 1
        self.state = 'turn' + str(self.players[self.turn%len(self.players)])

