import unittest

import numpy as np

from classic_games.tictactoe.model.board import TicTacToeBoard


class TestTicTacToeBoard(unittest.TestCase):
    """
    Tests the class TicTacToeBoard.
    """

    def setUp(self):
        # Non-terminated board
        self.board = TicTacToeBoard(
            board=np.array([[0, 1, 0], [1, -1, 1], [-1, 1, -1]]),
            your_start=False,
        )
        # terminated board
        self.terminated_board = TicTacToeBoard(
            board=np.array([[1, 1, 1], [1, -1, 1], [-1, 1, -1]]),
            your_start=False,
        )

    def test_row(self):
        """
        Tests the property row().
        """
        self.assertEqual(3, self.board.row)

    def test_col(self):
        """
        Tests the property col().
        """
        self.assertEqual(3, self.board.col)

    def test_check_terminated(self):
        """
        Tests the method check_terminated().
        """
        non_terminated = self.board.check_terminated()
        terminated = self.terminated_board.check_terminated()
        self.assertFalse(non_terminated)
        self.assertTrue(terminated)

    def test_check_winner(self):
        """
        Tests the method check_winner().
        """
        draw = self.board.check_winner()
        winner = self.terminated_board.check_winner()
        self.assertEqual(0, draw)
        self.assertEqual(self.board._your_symbol, winner)

    def test_get_current(self):
        """
        Tests the method get_current().
        """
        np.testing.assert_array_equal(np.array([[0, 1, 0], [1, -1, 1], [-1, 1, -1]]), self.board.get_current())
        np.testing.assert_array_equal(np.array([[1, 1, 1], [1, -1, 1], [-1, 1, -1]]), self.terminated_board.get_current())

    def test_get_successors(self):
        """
        Tests the method get_successors().
        """
        successors = self.board.get_successors()
        self.assertEqual(2, len(successors))
        np.testing.assert_array_equal(np.array([[-1, 1, 0], [1, -1, 1], [-1, 1, -1]]), successors[0])
        np.testing.assert_array_equal(np.array([[0, 1, -1], [1, -1, 1], [-1, 1, -1]]), successors[1])

    def test_get_history(self):
        """
        Tests the method get_history().
        """
        # Set on (0, 0) tile := -1 and on (0, 2) tile:= 1
        self.board.set(0)
        self.board.set(2)

        board_history = self.board.get_history()
        self.assertEqual(3, len(board_history))
        np.testing.assert_array_equal(np.array([[0, 1, 0], [1, -1, 1], [-1, 1, -1]]), board_history[0])
        np.testing.assert_array_equal(np.array([[-1, 1, 0], [1, -1, 1], [-1, 1, -1]]), board_history[1])
        np.testing.assert_array_equal(np.array([[-1, 1, 1], [1, -1, 1], [-1, 1, -1]]), board_history[2])

        terminated_history = self.terminated_board.get_history()
        self.assertEqual(1, len(terminated_history))
        np.testing.assert_array_equal(np.array([[1, 1, 1], [1, -1, 1], [-1, 1, -1]]), terminated_history[0])

    def test_get_actions(self):
        """
        Tests the method get_actions().
        """
        actions = self.board.get_actions()
        self.assertEqual([0, 2], actions)

    def test_get_current_player(self):
        """
        Tests the method get_current_player().
        """
        self.assertFalse(self.board.get_current_player())
        self.assertFalse(self.terminated_board.get_current_player())

    def test_set(self):
        """
        Tests the method set().
        """
        self.board.set(0)
        np.testing.assert_array_equal(np.array([[-1, 1, 0], [1, -1, 1], [-1, 1, -1]]), self.board.get_current())

    def test_get_reward(self):
        """
        Tests the method get_reward().
        """
        # Before calling get_reward() you have to check if it is terminated
        self.board.check_terminated()
        self.terminated_board.check_terminated()

        # Get the reward
        reward1 = self.board.get_reward()
        reward2 = self.terminated_board.get_reward()

        self.assertEqual(0.0, reward1)
        self.assertEqual(1.0, reward2)


if __name__ == '__main__':
    unittest.main()
