import unittest

from TicTacToe.agent.random_player import RandomPlayer
from TicTacToe.game.game import TicTacToeGame
from TicTacToe.model.board import Board


class TestRandomPlayer(unittest.TestCase):
    """
    Tests the class RandomPlayer and its methods.
    """

    def setUp(self):
        self.board = Board(height=3, width=3)
        self.game = TicTacToeGame(self.board, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=3)
        self.random_player = RandomPlayer(seed=0)

    def test_name(self):
        """
        Tests the property name() of class RandomPlayer
        """
        self.assertEqual("Random Player", self.random_player.name)

    def test_start(self):
        """
        Tests the method start() of class RandomPlayer.
        """
        action = self.random_player.act(turn=0, game=self.game, symbol=1)
        self.assertEqual(5, action)

    def test_act(self):
        """
        Tests the method act() of class RandomPlayer.
        """
        action = self.random_player.act(turn=0, game=self.game, symbol=1)
        self.assertEqual(5, action)

    def test_end(self):
        """
        Tests the method end() of class RandomPlayer. (Not necessary now!)
        """
        pass


if __name__ == '__main__':
    unittest.main()
