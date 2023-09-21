import unittest
import numpy as np

from classic_games.tictactoe.model.render import TicTacToeRender


class TestTicTacToeRender(unittest.TestCase):
    """
    Tests the class TicTacToeRender.
    """

    def setUp(self):
        self.human_render = TicTacToeRender(
            window_shape=(400, 600),
            board_shape=(3, 3),
            mode="human",
            your_symbol=1,
            enemy_symbol=-1,
        )

        self.rgb_render = TicTacToeRender(
            window_shape=(400, 600),
            board_shape=(3, 3),
            mode="rgb_array",
            your_symbol=1,
            enemy_symbol=-1,
        )

    def test_window_height(self):
        """
        Tests the property window_height.
        """
        self.assertEqual(400, self.human_render.window_height)

    def test_window_width(self):
        """
        Tests the property window_width.
        """
        self.assertEqual(600, self.human_render.window_width)

    def test_board_height(self):
        """
        Tests the property board_height.
        """
        self.assertEqual(3, self.human_render.board_height)

    def test_board_width(self):
        """
        Tests the property board_width.
        """
        self.assertEqual(3, self.human_render.board_width)

    def test_get_rgb_array(self):
        """
        Tests the method get_rgb_array().
        """
        board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        self.rgb_render.init()
        self.assertEqual((400, 600, 3), self.rgb_render.get_rgb_array(board).shape)

    def test_draw_step(self):
        """
        Tests the method draw_step()
        """
        history = [
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
        self.human_render.init()
        self.human_render.draw_step(history)


if __name__ == '__main__':
    unittest.main()
