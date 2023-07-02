import os
import unittest

import numpy as np

from TicTacToe.model.board import Board


class TestBoard(unittest.TestCase):
    """
    Tests the class Board and its methods.
    """

    def setUp(self):
        self.width = 3
        self.height = 3
        self.board = Board(self.width, self.height)

    def test_shape(self):
        """
        Tests the property shape of class Board.
        """
        self.assertEqual((self.height, self.width), self.board.shape)

    def test_total_history(self):
        """
        Tests the property total_history of class Board.
        """
        np.testing.assert_array_equal(self.board.history + [self.board.grid], self.board.total_history)

    def test_state_current(self):
        """
        Tests the method state() of class Board,
        where we want to have the current state (n=0).
        """
        np.testing.assert_array_equal(self.board.grid, self.board.state())

    def test_state_previous(self):
        """
        Tests the property state of class Board,
        where we want to have the first previous state (n=1).
        Board (after using all set_value_at() methods):
        |1|1|0|
        |0|0|0|
        |0|0|0|
        """
        # Set the board with values
        self.board.set_value_at(0, 0, 1)
        self.board.set_value_at(0, 1, 1)
        np.testing.assert_array_equal(self.board.history[-1], self.board.state(1))

    def test_set_value_at(self):
        """
        Tests the method set_value_at() in class Board.
        Board (after using all set_value_at() methods):
        |1|1|1|
        |0|0|0|
        |0|0|0|
        """
        self.board.set_value_at(0, 0, 1)
        self.board.set_value_at(0, 1, 1)
        self.board.set_value_at(0, 2, 1)
        self.board.set_value_at(0, 0, -1, check_empty=True)
        self.board.set_value_at(-1, -1, -1, check_range=True)

        self.assertEqual(1, self.board.grid[0][0])
        self.assertEqual(1, self.board.grid[0][1])
        self.assertEqual(1, self.board.grid[0][2])

        self.assertEqual(3, len(self.board.history))

    def test_get_value_at(self):
        """
        Tests the method get_value_at() in class Board.
        Board (after using all set_value_at() methods):
        |-2|1|-2|
        |1|-1|1|
        |-2|1|-2|
        """
        # Set the board with values
        self.board.set_value_at(0, 0, -2)
        self.board.set_value_at(0, 1, 1)
        self.board.set_value_at(0, 2, -2)
        self.board.set_value_at(1, 0, 1)
        self.board.set_value_at(1, 1, -1)
        self.board.set_value_at(1, 2, 1)
        self.board.set_value_at(2, 0, -2)
        self.board.set_value_at(2, 1, 1)
        self.board.set_value_at(2, 2, -2)

        self.assertEqual(-2, self.board.get_value_at(0, 0))
        self.assertEqual(-1, self.board.get_value_at(1, 1))
        self.assertEqual(1, self.board.get_value_at(1, 2))
        self.assertEqual(-2, self.board.get_value_at(2, 2))
        self.assertIsNone(self.board.get_value_at(-1, -1, check_range=True))

    def test_is_valid_at(self):
        """
        Tests the method is_valid_at() in class Board.
        Board:
        |0|0|0|
        |0|0|0|
        |0|0|0|
        """
        self.assertTrue(self.board.is_valid_at(0, 0))
        self.assertTrue(self.board.is_valid_at(1, 1))
        self.assertTrue(self.board.is_valid_at(1, 2))
        self.assertTrue(self.board.is_valid_at(2, 2))
        self.assertFalse(self.board.is_valid_at(-1, -1))

    def test_is_empty_at(self):
        """
        Tests the method is_empty_at() in class Board.
        Board (after using all set_value_at() methods):
        |0|1|-1|
        |0|1|-1|
        |0|1|-1|
        """
        # Set the board with values
        self.board.set_value_at(0, 1, 1)
        self.board.set_value_at(1, 1, 1)
        self.board.set_value_at(2, 1, 1)
        self.board.set_value_at(0, 2, -1)
        self.board.set_value_at(1, 2, -1)
        self.board.set_value_at(2, 2, -1)

        self.assertTrue(self.board.is_empty_at(0, 0))
        self.assertFalse(self.board.is_empty_at(1, 1))
        self.assertFalse(self.board.is_empty_at(1, 2))
        self.assertFalse(self.board.is_empty_at(2, 2))
        self.assertIsNone(self.board.is_empty_at(-1, -1, check_range=True))

    def test_is_full(self):
        """
        Tests the method is_full() in class Board.
        Board (after using all set_value_at() methods):
        |2|1|-1|
        |2|1|-1|
        |2|1|-1|
        """
        # Make the grid full of entries
        self.board.set_value_at(0, 0, 2)
        self.board.set_value_at(1, 0, 2)
        self.board.set_value_at(2, 0, 2)
        self.board.set_value_at(0, 1, 1)
        self.board.set_value_at(1, 1, 1)
        self.board.set_value_at(2, 1, 1)
        self.board.set_value_at(0, 2, -1)
        self.board.set_value_at(1, 2, -1)
        self.board.set_value_at(2, 2, -1)
        self.assertTrue(self.board.is_full())

    def test_save_and_load_board(self):
        """
        Tests the method save_board() and load_board() of class Board.
        """
        # Test method save_board()
        self.board.save_board("test")
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), "test.json")))

        # Test method load_board
        board = Board.load_board("test")
        self.assertEqual(self.board, board)


if __name__ == '__main__':
    unittest.main()
