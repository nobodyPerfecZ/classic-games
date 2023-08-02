import unittest
import numpy as np

from classic_games.tictactoe.agent.random_player import RandomPlayer


class TestRandomPlayer(unittest.TestCase):
    """
    Tests the class RandomPlayer.
    """

    def setUp(self):
        self.player = RandomPlayer(
            your_symbol=-1,
            enemy_symbol=1,
            tiles_to_win=3,
            seed=0
        )

        # Current board state
        self.board = np.array([
            [0, -1, 1],
            [0, 1, -1],
            [1, -1, 1],
        ])

    def test_name(self):
        """
        Tests the property name()
        """
        self.assertEqual("Random Player", self.player.name)

    def test_start(self):
        """
        Tests the method start()
        """
        action = self.player.start(self.board)
        self.assertEqual(0, action)

    def test_act(self):
        """
        Tests the method act()
        """
        action1 = self.player.act(self.board)  # should call start() first
        action2 = self.player.act(self.board)  # should now call act()
        self.assertEqual(0, action1)
        self.assertEqual(3, action2)

    def test_end(self):
        """
        Tests the method end().
        """
        pass


if __name__ == '__main__':
    unittest.main()
