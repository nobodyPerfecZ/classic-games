import time
import unittest
import numpy as np

from classic_games.tictactoe.agent.min_max_playerC import MiniMaxC, MinMaxPlayerC


class TestMiniMaxC(unittest.TestCase):
    """
    Tests the class MiniMaxC.
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

        self.minimax3x3 = MiniMaxC(
            your_symbol=1,
            enemy_symbol=-1,
            tiles_to_win=3,
        )
        self.minimax4x4 = MiniMaxC(
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


class TestMinMaxPlayerC(unittest.TestCase):
    """
    Tests the class MinMaxPlayerC.
    """

    def setUp(self):
        self.player = MinMaxPlayerC(
            your_symbol=1,
            enemy_symbol=-1,
            tiles_to_win=3,
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


if __name__ == "__main__":
    unittest.main()
