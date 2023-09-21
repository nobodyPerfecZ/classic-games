import unittest
import numpy as np

from classic_games.tictactoe.model.boardC import TicTacToeBoardC


class TestTicTacToeBoardC(unittest.TestCase):
    """
    Tests the class TicTacToeBoardC.
    """

    def setUp(self):
        # Non-terminated board (3x3)
        self.board3x3 = TicTacToeBoardC(
            board=np.array([
                [0, 1, 0],
                [1, -1, 1],
                [-1, 1, -1]
            ]),
            your_start=False,
        )
        # terminated board (3x3)
        self.terminated_board3x3 = TicTacToeBoardC(
            board=np.array([
                [1, 1, 1],
                [1, -1, 1],
                [-1, 1, -1]
            ]),
            your_start=False,
        )
        # Non-terminated board (4x4)
        self.board4x4 = TicTacToeBoardC(
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
        self.terminated_board4x4 = TicTacToeBoardC(
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
        self.assertEqual(4, self.board4x4.row)

    def test_col(self):
        """
        Tests the property col().
        """
        self.assertEqual(3, self.board3x3.col)
        self.assertEqual(4, self.board4x4.col)

    def test_check_terminated(self):
        """
        Tests the method check_terminated().
        """
        non_terminated3x3 = self.board3x3.check_terminated()
        non_terminated4x4 = self.board4x4.check_terminated()
        terminated3x3 = self.terminated_board3x3.check_terminated()
        terminated4x4 = self.terminated_board4x4.check_terminated()
        self.assertFalse(non_terminated3x3)
        self.assertFalse(non_terminated4x4)
        self.assertTrue(terminated3x3)
        self.assertTrue(terminated4x4)

    def test_check_winner(self):
        """
        Tests the method check_winner().
        """
        draw3x3 = self.board3x3.check_winner()
        draw4x4 = self.board4x4.check_winner()
        winner3x3 = self.terminated_board3x3.check_winner()
        winner4x4 = self.terminated_board4x4.check_winner()
        self.assertEqual(0, draw3x3)
        self.assertEqual(0, draw4x4)
        self.assertEqual(1, winner3x3)
        self.assertEqual(1, winner4x4)

    def test_get_current(self):
        """
        Tests the method get_current().
        """
        np.testing.assert_array_equal(np.array([[0, 1, 0], [1, -1, 1], [-1, 1, -1]]),
                                      self.board3x3.get_current())
        np.testing.assert_array_equal(np.array([[1, 1, 1, 0], [1, -1, 1, 0], [-1, -1, -1, 0], [0, 0, 0, 0]]),
                                      self.board4x4.get_current())
        np.testing.assert_array_equal(np.array([[1, 1, 1], [1, -1, 1], [-1, 1, -1]]),
                                      self.terminated_board3x3.get_current())
        np.testing.assert_array_equal(np.array([[1, 1, -1, 1], [1, -1, 1, 1], [-1, 1, -1, -1], [1, -1, 1, -1]]),
                                      self.terminated_board4x4.get_current())

    def test_get_successors(self):
        """
        Tests the method get_successors().
        """
        successors3x3 = self.board3x3.get_successors()
        self.assertEqual(2, len(successors3x3))
        self.assertEqual(False, self.board3x3.get_current_player())  # check if current player gets changed
        self.assertEqual(1, len(self.board3x3.get_history()))  # check if history gets changed
        np.testing.assert_array_equal(np.array([[-1, 1, 0], [1, -1, 1], [-1, 1, -1]]), successors3x3[0])
        np.testing.assert_array_equal(np.array([[0, 1, -1], [1, -1, 1], [-1, 1, -1]]), successors3x3[1])

        successors4x4 = self.board4x4.get_successors()
        self.assertEqual(7, len(successors4x4))
        self.assertEqual(False, self.board4x4.get_current_player())
        self.assertEqual(1, len(self.board4x4.get_history()))
        np.testing.assert_array_equal(np.array([[1, 1, 1, -1], [1, -1, 1, 0], [-1, -1, -1, 0], [0, 0, 0, 0]]),
                                      successors4x4[0])
        np.testing.assert_array_equal(np.array([[1, 1, 1, 0], [1, -1, 1, -1], [-1, -1, -1, 0], [0, 0, 0, 0]]),
                                      successors4x4[1])
        np.testing.assert_array_equal(np.array([[1, 1, 1, 0], [1, -1, 1, 0], [-1, -1, -1, -1], [0, 0, 0, 0]]),
                                      successors4x4[2])
        np.testing.assert_array_equal(np.array([[1, 1, 1, 0], [1, -1, 1, 0], [-1, -1, -1, 0], [-1, 0, 0, 0]]),
                                      successors4x4[3])
        np.testing.assert_array_equal(np.array([[1, 1, 1, 0], [1, -1, 1, 0], [-1, -1, -1, 0], [0, -1, 0, 0]]),
                                      successors4x4[4])
        np.testing.assert_array_equal(np.array([[1, 1, 1, 0], [1, -1, 1, 0], [-1, -1, -1, 0], [0, 0, -1, 0]]),
                                      successors4x4[5])
        np.testing.assert_array_equal(np.array([[1, 1, 1, 0], [1, -1, 1, 0], [-1, -1, -1, 0], [0, 0, 0, -1]]),
                                      successors4x4[6])

    def test_get_history(self):
        """
        Tests the method get_history().
        """
        self.board3x3.set(0)
        self.board3x3.set(2)
        self.assertEqual(3, len(self.board3x3.get_history()))
        np.testing.assert_array_equal(np.array([[0, 1, 0], [1, -1, 1], [-1, 1, -1]]), self.board3x3.get_history()[0])
        np.testing.assert_array_equal(np.array([[-1, 1, 0], [1, -1, 1], [-1, 1, -1]]), self.board3x3.get_history()[1])
        np.testing.assert_array_equal(np.array([[-1, 1, 1], [1, -1, 1], [-1, 1, -1]]), self.board3x3.get_history()[2])

        self.board4x4.set(3)
        self.board4x4.set(12)
        self.assertEqual(3, len(self.board4x4.get_history()))
        np.testing.assert_array_equal(np.array([[1, 1, 1, 0], [1, -1, 1, 0], [-1, -1, -1, 0], [0, 0, 0, 0]]),
                                      self.board4x4.get_history()[0])
        np.testing.assert_array_equal(np.array([[1, 1, 1, -1], [1, -1, 1, 0], [-1, -1, -1, 0], [0, 0, 0, 0]]),
                                      self.board4x4.get_history()[1])
        np.testing.assert_array_equal(np.array([[1, 1, 1, -1], [1, -1, 1, 0], [-1, -1, -1, 0], [1, 0, 0, 0]]),
                                      self.board4x4.get_history()[2])

    def test_get_actions(self):
        """
        Tests the method get_actions().
        """
        actions3x3 = self.board3x3.get_actions()
        empty_actions3x3 = self.terminated_board3x3.get_actions()
        actions4x4 = self.board4x4.get_actions()
        empty_actions4x4 = self.terminated_board4x4.get_actions()
        self.assertEqual([0, 2], actions3x3)
        self.assertEqual([], empty_actions3x3)
        self.assertEqual([3, 7, 11, 12, 13, 14, 15], actions4x4)
        self.assertEqual([], empty_actions4x4)

    def test_get_current_player(self):
        """
        Tests the method get_current_player().
        """
        self.assertFalse(self.board3x3.get_current_player())
        self.assertFalse(self.terminated_board3x3.get_current_player())
        self.assertFalse(self.board4x4.get_current_player())
        self.assertFalse(self.terminated_board4x4.get_current_player())

    def test_set(self):
        """
        Tests the method set().
        """
        self.board3x3.set(0)
        self.assertTrue(self.board3x3.get_current_player())  # check if current player gets updated
        self.assertEqual(2, len(self.board3x3.get_history()))  # check if history gets updated
        np.testing.assert_array_equal(np.array([[-1, 1, 0], [1, -1, 1], [-1, 1, -1]]), self.board3x3.get_history()[-1])
        np.testing.assert_array_equal(np.array([[-1, 1, 0], [1, -1, 1], [-1, 1, -1]]), self.board3x3.get_current())

        self.board4x4.set(3)
        self.assertTrue(self.board4x4.get_current_player())
        self.assertEqual(2, len(self.board4x4.get_history()))
        np.testing.assert_array_equal(np.array([[1, 1, 1, -1], [1, -1, 1, 0], [-1, -1, -1, 0], [0, 0, 0, 0]]),
                                      self.board4x4.get_history()[-1])
        np.testing.assert_array_equal(np.array([[1, 1, 1, -1], [1, -1, 1, 0], [-1, -1, -1, 0], [0, 0, 0, 0]]),
                                      self.board4x4.get_current())

    def test_get_reward(self):
        """
        Tests the method get_reward().
        """
        # Before calling get_reward() you have to check if it is terminated
        self.board3x3.check_terminated()
        self.terminated_board3x3.check_terminated()
        self.board4x4.check_terminated()
        self.terminated_board4x4.check_terminated()

        self.assertEqual(0.0, self.board3x3.get_reward())
        self.assertEqual(1.0, self.terminated_board3x3.get_reward())
        self.assertEqual(0.0, self.board4x4.get_reward())
        self.assertEqual(1.0, self.terminated_board4x4.get_reward())

    def test_get_immediate_winning_moves(self):
        """
        Tests the method get_immediate_winning_moves().
        """
        immediate_winning_moves3x3 = self.board3x3.get_immediate_winning_moves()
        immediate_winning_moves4x4 = self.board4x4.get_immediate_winning_moves()

        self.assertEqual(0, immediate_winning_moves3x3)
        self.assertEqual(1, immediate_winning_moves4x4)

    def test_get_immediate_blocking_moves(self):
        """
        Tests the method get_immediate_blocking_moves().
        """
        immediate_blocking_moves3x3 = self.board3x3.get_immediate_blocking_moves()
        immediate_blocking_moves4x4 = self.board4x4.get_immediate_blocking_moves()

        self.assertEqual(2, immediate_blocking_moves3x3)
        self.assertEqual(1, immediate_blocking_moves4x4)
