from flask_socketio import SocketIO, send, emit, join_room, leave_room

from board import Board
from game_controller import GameController
from moveValidator import MoveValidator, GameStrategy, GameStrategy1
from bot import Bot


class Lobby:
    def __init__(self, lobby_name: str, needed_players: int, bot_count: int, game_strategy: GameStrategy, socketio: SocketIO):
        self.socketio = socketio
        self.name = lobby_name
        self.players = []
        self.player_count = needed_players
        self.board = Board(needed_players)
        self.game_controller = GameController(needed_players)
        self.move_validator = MoveValidator(game_strategy)
        self.bots = [Bot(needed_players - int(bot_count) + i + 1, game_strategy) for i in range(int(bot_count))]
        self.bot_count = int(bot_count)
        self._add_bots()

    def _add_bots(self):
        for bot in self.bots:
            self.players.append(f'Bot {bot.player}')

    def add_player(self, player: str):
        if len(self.players) < self.player_count:
            self.players.append(player)
            return True
        return False

    def start_game(self):
        # Ensure the first player is not a bot
        if self.players[0].startswith('Bot'):
            for i in range(1, len(self.players)):
                if not self.players[i].startswith('Bot'):
                    # Swap the first player with the first human player found
                    self.players[0], self.players[i] = self.players[i], self.players[0]
                    break

        self.game_controller.start_game()


    def set_game_strategy(self, game_strategy: GameStrategy):
            self.move_validator.game_strategy(game_strategy)

    def remove_player(self, player: str):
        self.players.remove(player)

    def is_full(self):
        return len(self.players) >= self.player_count

    def next_turn(self):
        self.game_controller.next_turn()
        current_player = self.game_controller.get_current_player()
        if current_player >= self.player_count and self.bot_count > 0:
            move = self.bots[current_player - self.player_count].make_move(self.board)
            print('Bot move:', move)
            # Move logic
            self.board.flatarr[move].content = self.board.selected.content
            self.board.decrease_player_pieces(self.board.selected.content)
            self.board.selected.content = 0

            if move is not None:
                self.broadcast_bot_move(move)
        return current_player

    def broadcast_bot_move(self, move):
        self.socketio.emit('update_board', {'board': self.board.board_to_data()}, room=self.name)
        if self.move_validator.check_for_win(self.board, self.game_controller.get_current_player()):
            self.set_winner(f'Bot {self.game_controller.get_current_player()}')
            self.socketio.emit('update_state', {'state': f'wonBot{self.game_controller.get_current_player()}'}, room=self.name)
            self.socketio.emit('chat_message', {
                'username': 'server',
                'message': f'Bot {self.game_controller.get_current_player()} has won the game!'
            }, room=self.name)
        else:
            self.next_turn()

    def set_winner(self, player):
        self.game_controller.set_winner(player)

    def get_state(self):
        return self.game_controller.current_state
