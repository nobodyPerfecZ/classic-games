import os
import unittest

from TicTacToe.model.board import Board
from TicTacToe.tests.model.test_grid_map import TestGridMap


class TestBoard(TestGridMap):

    def setUp(self):
        super().setUp()
        self.board = Board(self.height, self.width, grid=self.grid.grid)

    def test_set_value_at(self):
        self.board.set_value_at(0, 0, 2)

        self.assertEqual(2, self.board.get_value_at(0, 0))
        self.assertEqual(1, self.board.turn)
        self.assertEqual(1, len(self.board.history))

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
