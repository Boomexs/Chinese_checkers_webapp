from board import Board
from game_controller import GameController
from moveValidator import MoveValidator, GameStrategy, GameStrategy1


class Lobby:
    def __init__(self, lobby_name: str, needed_players: int, game_strategy: GameStrategy):
        self.name = lobby_name
        self.players = []
        self.player_count = needed_players
        self.board = Board(needed_players)
        self.game_controller = GameController(needed_players)
        self.move_validator = MoveValidator(game_strategy)

    def add_player(self, player: str):
        if len(self.players) < self.player_count:
            self.players.append(player)
            return True
        return False

    def set_game_strategy(self, game_strategy: GameStrategy):
        self.move_validator.game_strategy(game_strategy)

    def remove_player(self, player: str):
        self.players.remove(player)

    def is_full(self):
        return len(self.players) >= self.player_count

    def next_turn(self):
        self.game_controller.next_turn()
        current_player = self.game_controller.get_current_player()
        return current_player

    def set_winner(self, player):
        self.game_controller.set_winner(player)

    def get_state(self):
        return self.game_controller.current_state
