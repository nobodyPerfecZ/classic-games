import unittest

import numpy as np

from classic_games.tictactoe.agent.min_max_player import MinMaxPlayer


class TestMinMaxPlayer(unittest.TestCase):
    """
    Tests the class MinMaxPlayer.
    """

    def setUp(self):
        self.player = MinMaxPlayer(
            your_symbol=1,
            enemy_symbol=-1,
            tiles_to_win=3,
            seed=0
        )

        # Current board state
        self.board = np.array([
            [0, -1, 1],
            [0, 0, -1],
            [1, -1, 1],
        ])

        # Losing state board
        self.board2 = np.array([
            [0, 0, 0],
            [-1, -1, 0],
            [0, 0, 0],
        ])

        self.board3 = np.array([
            [-1, 1, -1],
            [-1, 1, 0],
            [0, 0, 1],
        ])

    def test_name(self):
        """
        Tests the property name.
        """
        self.assertEqual("MinMax Player", self.player.name)

    def test_start(self):
        """
        Tests the method start().
        """
        action1 = self.player.start(self.board)
        action2 = self.player.start(self.board2)
        action3 = self.player.start(self.board3)

        self.assertEqual(4, action1)
        self.assertEqual(5, action2)
        self.assertEqual(7, action3)

    def test_act(self):
        """
        Tests the method act().
        """
        action1 = self.player.act(self.board)  # should call start() first
        action2 = self.player.act(self.board2)  # should now call act()
        action3 = self.player.act(self.board3)

        self.assertEqual(4, action1)
        self.assertEqual(5, action2)
        self.assertEqual(7, action3)

    def test_end(self):
        """
        Tests the method end().
        """
        pass


if __name__ == '__main__':
    unittest.main()
