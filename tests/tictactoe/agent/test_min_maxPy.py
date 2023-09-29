import time
import unittest
import numpy as np

from classic_games.tictactoe.agent.min_max import MiniMax


class TestMiniMax(unittest.TestCase):
    """
    Tests the (cython) class MiniMax.
    """

    def setUp(self):
        self.empty_board3x3 = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])
        self.board3x3 = np.array([
            [-1, 1, -1],
            [-1, 1, 0],
            [0, 0, 1],
        ])
        self.empty_board4x4 = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        self.board4x4 = np.array([
            [-1, 1, -1, 0],
            [-1, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
        ])

        self.minimax3x3 = MiniMax(
            your_symbol=1,
            enemy_symbol=-1,
            tiles_to_win=3,
        )
        self.minimax4x4 = MiniMax(
            your_symbol=1,
            enemy_symbol=-1,
            tiles_to_win=4,
            max_depth=8,
        )

    def test_get_best_action(self):
        """
        Tests the method get_best_action().
        """
        self.assertEqual(0, self.minimax3x3.get_best_action(self.empty_board3x3))
        self.assertEqual(7, self.minimax3x3.get_best_action(self.board3x3))

        self.assertEqual(0, self.minimax4x4.get_best_action(self.empty_board4x4))
        self.assertEqual(3, self.minimax4x4.get_best_action(self.board4x4))

    def test_get_best_action_with_cache(self):
        """
        Tests the method get_best_action() by using the cache for already evaluated states.
        """
        action1 = self.minimax4x4.get_best_action(self.empty_board4x4)
        start_time = time.time()
        action2 = self.minimax4x4.get_best_action(self.empty_board4x4)
        end_time = time.time()

        self.assertEqual(action1, action2)
        self.assertLessEqual(end_time - start_time, 0.1)  # check if second call took less than 0.1 seconds of time


if __name__ == '__main__':
    unittest.main()
