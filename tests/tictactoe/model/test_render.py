import unittest

import numpy as np

from classic_games.tictactoe.model.render import TicTacToeRender


class TestTicTacToeRender(unittest.TestCase):
    """
    Tests the class TicTacToeRender.
    """

    def setUp(self):
        self.render = TicTacToeRender(
            window_shape=(400, 600),
            board_shape=(3, 3),
            your_symbol=1,
            enemy_symbol=-1,
        )

    def test_window_height(self):
        """
        Tests the property window_height.
        """
        self.assertEqual(400, self.render.window_height)

    def test_window_width(self):
        """
        Tests the property window_width.
        """
        self.assertEqual(600, self.render.window_width)

    def test_board_height(self):
        """
        Tests the property board_height.
        """
        self.assertEqual(3, self.render.board_height)

    def test_board_width(self):
        """
        Tests the property board_width.
        """
        self.assertEqual(3, self.render.board_width)

    def test_draw_game(self):
        """
        Tests the method draw_game()
        """
        states = [
            np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
            np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]),
            np.array([[1, -1, 0], [0, 0, 0], [0, 0, 0]]),
            np.array([[1, -1, 1], [0, 0, 0], [0, 0, 0]]),
            np.array([[1, -1, 1], [-1, 0, 0], [0, 0, 0]]),
            np.array([[1, -1, 1], [-1, 1, 0], [0, 0, 0]]),
            np.array([[1, -1, 1], [-1, 1, -1], [0, 0, 0]]),
            np.array([[1, -1, 1], [-1, 1, -1], [1, 0, 0]]),
            np.array([[1, -1, 1], [-1, 1, -1], [1, -1, 0]]),
            np.array([[1, -1, 1], [-1, 1, -1], [1, -1, 1]]),
        ]
        self.render.init()
        self.render.draw_game(states)


if __name__ == '__main__':
    unittest.main()
