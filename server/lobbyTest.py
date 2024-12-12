import unittest
from lobby import Lobby

class TestLobby(unittest.TestCase):
    def setUp(self):
        self.lobby = Lobby('lobby1', 6)
    def test_add_player(self):
        self.assertTrue(self.lobby.add_player('player1'))
        self.assertTrue(self.lobby.add_player('player2'))
        self.assertTrue(self.lobby.add_player('player3'))
        self.assertTrue(self.lobby.add_player('player4'))
        self.assertTrue(self.lobby.add_player('player5'))
        self.assertTrue(self.lobby.add_player('player6'))
        self.assertFalse(self.lobby.add_player('player7'))

    def test_remove_player(self):
        self.lobby.add_player('player1')
        self.lobby.add_player('player2')
        self.lobby.add_player('player3')
        self.lobby.add_player('player4')
        self.lobby.add_player('player5')
        self.lobby.add_player('player6')
        self.lobby.remove_player('player1')
        self.lobby.remove_player('player2')
        self.lobby.remove_player('player3')
        self.lobby.remove_player('player4')
        self.lobby.remove_player('player5')
        self.lobby.remove_player('player6')
        self.assertEqual(self.lobby.players, [])

if __name__ == '__main__':
    unittest.main()