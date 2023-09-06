import unittest
from unittest.mock import patch

import numpy as np

from classic_games.tictactoe.agent.human_player import HumanPlayer


class TestHumanPlayer(unittest.TestCase):
    """
    Tests the class HumanPlayer().
    """

    def setUp(self):
        self.player = HumanPlayer(
            your_symbol=1,
            enemy_symbol=1,
            tiles_to_win=3,
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
        self.assertEqual("Human Player", self.player.name)

    @patch('builtins.input', side_effect=['3'])
    def test_start(self, mock_input: str):
        """
        Tests the method start().
        """
        action = self.player.start(self.board)
        self.assertEqual(3, action)

    @patch("builtins.input", side_effect=["8", "0", "9", "3"])
    def test_act(self, mock_input: str):
        """
        Tests the method act().
        """
        action1 = self.player.act(self.board)  # should call start() first
        action2 = self.player.act(self.board)  # should now call act()
        self.assertEqual(0, action1)
        self.assertEqual(3, action2)


if __name__ == '__main__':
    unittest.main()
