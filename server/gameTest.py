from lobby import Lobby
import unittest
from board import Board
from moveValidator import GameStrategy1, MoveValidator


class TestGame(unittest.TestCase):
    def setUp(self):
        self.lobby = Lobby("test_lobby", 2, GameStrategy1())
        self.lobby.add_player("player1")
        self.lobby.add_player("player2")
        self.move_validator = MoveValidator(GameStrategy1())
        self.board = Board(2)
        self.players = {
            "player1": 1,
            "player2": 2
        }

    def test_turn(self):
        self.assertEqual(self.lobby.next_turn(), self.players["player2"])
        self.assertEqual(self.lobby.next_turn(), self.players["player1"])
        self.assertEqual(self.lobby.next_turn(), self.players["player2"])

    def test_winner(self):
        self.lobby.set_winner("player1")
        self.assertEqual(self.lobby.get_state(), "GameEnd")
        self.assertEqual(self.lobby.game_controller.winner, "player1")

    def test_player_moves_all_pieces_to_back_row(self):
        # Simulate moving all pieces of player 1 to the back row
        back_row = self.board.zones["down"]
        for cell in back_row:
            if cell is not None:
                cell.content = 1

        self.assertTrue(self.move_validator.check_for_win(self.board, 1))

        # Check if all pieces in the back row belong to player 1


if __name__ == '__main__':
    unittest.main()

