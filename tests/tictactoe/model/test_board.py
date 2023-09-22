import unittest
import numpy as np

from classic_games.tictactoe.model.board import TicTacToeBoard


class TestTicTacToeBoard(unittest.TestCase):
    """
    Tests the class TicTacToeBoard.
    """

    def setUp(self):
        # Non-terminated board
        self.board3x3 = TicTacToeBoard(
            board=np.array([
                [0, 1, 0], 
                [1, -1, 1], 
                [-1, 1, -1]
            ]),
            your_start=False,
        )
        # terminated board
        self.terminated_board3x3 = TicTacToeBoard(
            board=np.array([
                [1, 1, 1], 
                [1, -1, 1], 
                [-1, 1, -1]
            ]),
            your_start=False,
        )
        self.board4x4 = TicTacToeBoard(
            board=np.array([
                [1, 1, 1, 0],
                [1, -1, 1, 0],
                [-1, -1, -1, 0],
                [0, 0, 0, 0],
            ]),
            tiles_to_win=4,
            your_start=False,
        )
        # terminated board (4x4)
        self.terminated_board4x4 = TicTacToeBoard(
            board=np.array([
                [1, 1, -1, 1],
                [1, -1, 1, 1],
                [-1, 1, -1, -1],
                [1, -1, 1, -1],
            ]),
            tiles_to_win=4,
            your_start=False,
        )

    def test_row(self):
        """
        Tests the property row().
        """
        self.assertEqual(3, self.board3x3.row)

    def test_col(self):
        """
        Tests the property col().
        """
        self.assertEqual(3, self.board3x3.col)

    def test_check_terminated(self):
        """
        Tests the method check_terminated().
        """
        non_terminated = self.board3x3.check_terminated()
        terminated = self.terminated_board3x3.check_terminated()
        self.assertFalse(non_terminated)
        self.assertTrue(terminated)

    def test_check_winner(self):
        """
        Tests the method check_winner().
        """
        draw = self.board3x3.check_winner()
        winner = self.terminated_board3x3.check_winner()
        self.assertEqual(0, draw)
        self.assertEqual(self.board3x3._your_symbol, winner)

    def test_get_current(self):
        """
        Tests the method get_current().
        """
        np.testing.assert_array_equal(np.array([[0, 1, 0], [1, -1, 1], [-1, 1, -1]]), self.board3x3.get_current())
        np.testing.assert_array_equal(np.array([[1, 1, 1], [1, -1, 1], [-1, 1, -1]]), self.terminated_board3x3.get_current())

    def test_get_successors(self):
        """
        Tests the method get_successors().
        """
        successors = self.board3x3.get_successors()
        self.assertEqual(2, len(successors))
        self.assertEqual(False, self.board3x3.get_current_player())  # check if current player gets changed
        self.assertEqual(1, len(self.board3x3.get_history()))  # check if history gets changed
        np.testing.assert_array_equal(np.array([[-1, 1, 0], [1, -1, 1], [-1, 1, -1]]), successors[0])
        np.testing.assert_array_equal(np.array([[0, 1, -1], [1, -1, 1], [-1, 1, -1]]), successors[1])

    def test_get_history(self):
        """
        Tests the method get_history().
        """
        # Set on (0, 0) tile := -1 and on (0, 2) tile:= 1
        self.board3x3.set(0)
        self.board3x3.set(2)

        board_history = self.board3x3.get_history()
        self.assertEqual(3, len(board_history))
        np.testing.assert_array_equal(np.array([[0, 1, 0], [1, -1, 1], [-1, 1, -1]]), board_history[0])
        np.testing.assert_array_equal(np.array([[-1, 1, 0], [1, -1, 1], [-1, 1, -1]]), board_history[1])
        np.testing.assert_array_equal(np.array([[-1, 1, 1], [1, -1, 1], [-1, 1, -1]]), board_history[2])

        terminated_history = self.terminated_board3x3.get_history()
        self.assertEqual(1, len(terminated_history))
        np.testing.assert_array_equal(np.array([[1, 1, 1], [1, -1, 1], [-1, 1, -1]]), terminated_history[0])

    def test_get_actions(self):
        """
        Tests the method get_actions().
        """
        actions = self.board3x3.get_actions()
        self.assertEqual([0, 2], actions)

    def test_get_current_player(self):
        """
        Tests the method get_current_player().
        """
        self.assertFalse(self.board3x3.get_current_player())
        self.assertFalse(self.terminated_board3x3.get_current_player())

    def test_set(self):
        """
        Tests the method set().
        """
        self.board3x3.set(0)
        np.testing.assert_array_equal(np.array([[-1, 1, 0], [1, -1, 1], [-1, 1, -1]]), self.board3x3.get_current())

    def test_get_reward(self):
        """
        Tests the method get_reward().
        """
        # Before calling get_reward() you have to check if it is terminated
        self.board3x3.check_terminated()
        self.terminated_board3x3.check_terminated()

        # Get the reward
        reward1 = self.board3x3.get_reward()
        reward2 = self.terminated_board3x3.get_reward()

        self.assertEqual(0.0, reward1)
        self.assertEqual(1.0, reward2)

    def test_immediate_winning_moves(self):
        """
        Tests the method immediate_winning_moves().
        """
        immediate_winning_moves3x3 = self.board3x3.get_immediate_winning_moves()
        immediate_winning_moves4x4 = self.board4x4.get_immediate_winning_moves()

        self.assertEqual(0, immediate_winning_moves3x3)
        self.assertEqual(1, immediate_winning_moves4x4)

    def test_immediate_blocking_moves(self):
        """
        Tests the method immediate_blocking_moves().
        """
        immediate_blocking_moves3x3 = self.board3x3.get_immediate_blocking_moves()
        immediate_blocking_moves4x4 = self.board4x4.get_immediate_blocking_moves()

        self.assertEqual(2, immediate_blocking_moves3x3)
        self.assertEqual(1, immediate_blocking_moves4x4)


if __name__ == '__main__':
    unittest.main()
