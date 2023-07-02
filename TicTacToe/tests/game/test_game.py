import unittest

import numpy as np

from TicTacToe.agent.random_player import RandomPlayer
from TicTacToe.game.game import TicTacToeGame
from TicTacToe.model.board import Board


class TestTicTacToeGame(unittest.TestCase):

    def setUp(self):
        """
        Create a board with the following
        """
        grid_row = np.array([
            [1, -1, 1, -1],
            [0, 0, -1, -1],
            [1, 1, 1, 1],
            [0, -1, 1, -1],
        ])
        grid_column = np.array([
            [1, -1, 1, -1],
            [0, 0, 1, 0],
            [-1, -1, 1, -1],
            [0, -1, 1, -1],
        ])
        grid_diagonal = np.array([
            [-1, 0, -1, 1],
            [-1, -1, 1, -1],
            [1, 0, -1, 1],
            [1, 1, -1, -1],
        ])
        grid_anti_diagonal = np.array([
            [-1, 0, 0, -1],
            [-1, 0, -1, -1],
            [1, -1, 0, 1],
            [-1, 1, -1, -1],
        ])
        grid_no_same_tiles = np.array([
            [-1, 1, 0, -1],
            [1, -1, 0, 1],
            [1, -1, 0, 0],
            [1, -1, 0, 0],
        ])
        self.board_row = Board(grid=grid_row)
        self.board_column = Board(grid=grid_column)
        self.board_diagonal = Board(grid=grid_diagonal)
        self.board_anti_diagonal = Board(grid=grid_anti_diagonal)
        self.board_no_same_tiles = Board(grid=grid_no_same_tiles)

    """
    def test_(self):
        game = TicTacToeGame(board=Board(width=3, height=3), player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=3)
        game.reset()
        game.run()
    """

    def test_action_space(self):
        """
        Tests the property action_space() in class TicTacToeGame.
        """
        game = TicTacToeGame(board=self.board_row, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        self.assertEqual((4, 4), game.observation_space)

    def test_observation_space(self):
        """
        Tests the property observation_space() in class TicTacToeGame.
        """
        game = TicTacToeGame(board=self.board_row, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        self.assertEqual((16,), game.action_space)

    def test_reset(self):
        """
        Tests the method reset() in class TicTacToeGame.
        """
        game = TicTacToeGame(board=self.board_row, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        game.reset()
        self.assertEqual(0, game.curr_turn)
        np.testing.assert_array_equal(np.zeros(shape=game.board.shape, dtype=int), game.board.state())

    def test_turn(self):
        """
        Tests the method turn() in class TicTacToeGame.
        """
        game = TicTacToeGame(board=self.board_row, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        game.reset()
        game.turn()
        self.assertEqual(1, game.curr_turn)
        self.assertEqual(1, len(game.board.history))

    def test_finished(self):
        """
        Tests the method finished() in class TicTacToeGame.
        """
        game = TicTacToeGame(board=self.board_row, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        terminated, winner = game.finished()
        self.assertTrue(terminated)
        self.assertEqual(game.player1_symbol, winner)

    def test_terminated(self):
        """
        Tests the method terminated() in class TicTacToeGame.
        """
        game = TicTacToeGame(board=self.board_row, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        terminated = game.terminated()
        self.assertFalse(terminated)

    def test_run(self):
        """
        Tests the method run() in class TicTacToeGame.
        """
        pass

    def test_get_observation(self):
        """
        Tests the method get_observation() in class TicTacToeGame.
        """
        game = TicTacToeGame(board=self.board_row, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        obs = game.get_observation()
        np.testing.assert_array_equal(game.board.state(), obs)

    def test_get_valid_actions(self):
        """
        Tests the method get_valid_actions() in class TicTacToeGame.
        """
        game = TicTacToeGame(board=self.board_row, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        actions = game.get_valid_actions()
        np.testing.assert_array_equal(np.array([4, 5, 12]), actions)

    def test_is_valid_action(self):
        """
        Tests the method is_valid_action() in class TicTacToeGame.
        """
        game = TicTacToeGame(board=self.board_row, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        is_valid1 = game.is_valid_action(0)
        is_valid2 = game.is_valid_action(4)

        self.assertFalse(is_valid1)
        self.assertTrue(is_valid2)

    def test_check_winner_row(self):
        """
        Tests the method check_winner() in class TicTacToeGame,
        where the n same tiles are in a row.
        """
        game = TicTacToeGame(self.board_row, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        actual = game.check_winner(n=4)
        self.assertEqual(game.player1_symbol, actual)

    def test_check_winners_column(self):
        """
        Tests the method check_winner() in class TicTacToeGame,
        where the n same tiles are in a column.
        """
        game = TicTacToeGame(self.board_column, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        actual = game.check_winner(n=4)
        self.assertEqual(game.player1_symbol, actual)

    def test_check_winner_diagonal(self):
        """
        Tests the method check_winner() in class TicTacToeGame,
        where the n same tiles are in a diagonal.
        """
        game = TicTacToeGame(self.board_diagonal, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        actual = game.check_winner(n=4)
        self.assertEqual(game.player2_symbol, actual)

    def test_check_winner_anti_diagonal(self):
        """
        Tests the method check_winner() in class TicTacToeGame,
        where the n same tiles are in an anti-diagonal.
        """
        game = TicTacToeGame(self.board_anti_diagonal, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        actual = game.check_winner(n=4)
        self.assertEqual(game.player2_symbol, actual)

    def test_check_winner_tiles_none(self):
        """
        Tests the method check_winner() in class TicTacToeGame,
        where no n same tiles are provided.
        """
        game = TicTacToeGame(self.board_no_same_tiles, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        actual = game.check_winner(n=4)
        self.assertEqual(0, actual)

    def test_to_tile(self):
        """
        Tests the method to_tile() in class TicTacToeGame.
        """
        game = TicTacToeGame(self.board_no_same_tiles, player1=RandomPlayer(), player2=RandomPlayer(), n_tiles=4)
        tuple1 = game.to_tile(0)
        tuple2 = game.to_tile(6)

        self.assertEqual((0, 0), tuple1)
        self.assertEqual((1, 2), tuple2)


if __name__ == '__main__':
    unittest.main()
