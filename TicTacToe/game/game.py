import numpy as np

from TicTacToe.agent.abstract_player import Player
from TicTacToe.game.abstract_game import Game
from TicTacToe.model.board import Board


class TicTacToeGame(Game):

    def __init__(
            self,
            board: Board,
            player1: Player,
            player2: Player,
            player1_symbol: int = 1,
            player2_symbol: int = -1,
            n_tiles: int = 3,
    ):
        assert board is not None, "#ERROR_GAME: Board should be given!"
        assert player1 is not None or player2 is not None, "#ERROR_GAME: Player1 and Player2 should be given!"
        assert player1_symbol != 0 and player2_symbol != 0, \
            "#ERROR_GAME: Symbol of player1 and player2 should not be 0!"
        assert player1_symbol != player2_symbol, "#ERROR_GAME: Symbol of player1 and player2 should be different!"
        assert 3 <= n_tiles <= board.shape[0] and n_tiles <= board.shape[1], \
            "#ERROR_GAME: n_tiles (#tiles to win) should be higher/equal than 3 and lower/equal to the board shape!"
        self.curr_turn = 0  # current turn
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.player1_symbol = player1_symbol
        self.player2_symbol = player2_symbol
        self.n_tiles = n_tiles

    @property
    def observation_space(self) -> np.ndarray:
        return self.board.shape

    @property
    def action_space(self) -> np.ndarray:
        return self.board.state().reshape(-1).shape

    def reset(self):
        self.curr_turn = 0
        self.board = Board(height=self.board.shape[0], width=self.board.shape[1])

    def turn(self):
        # Get the action from the current player
        if self.curr_turn == 0:
            # Case: First move of first player
            action = self.player1.start(self.curr_turn, self, self.player1_symbol)
            symbol = self.player1_symbol
        elif self.curr_turn == 1:
            # Case: First move of second player
            action = self.player2.start(self.curr_turn, self, self.player2_symbol)
            symbol = self.player2_symbol
        elif (self.curr_turn % 2) == 0:
            # Case: First player has to move
            action = self.player1.act(self.curr_turn, self, self.player1_symbol)
            symbol = self.player1_symbol
        else:
            # Case: Second player has to move
            action = self.player2.act(self.curr_turn, self, self.player2_symbol)
            symbol = self.player2_symbol

        if not self.is_valid_action(action):
            raise ValueError("ERROR_GAME: Action is not valid!")

        # Convert action into Position (y, x)
        y, x = self.to_tile(action)

        # Update the board
        self.board.set_value_at(y, x, symbol)

        # Update player next turn
        self.curr_turn += 1

    def finished(self) -> tuple[bool, int]:
        winner = self.check_winner(n=self.n_tiles)
        terminated = self.terminated()

        if winner != 0:
            # Case: Player1 or Player2 won the game
            return True, winner
        elif terminated:
            # Case: Either Player1 or Player2 won the game
            return terminated, 0
        else:
            # Case: Game is still running
            return False, 0

    def terminated(self) -> bool:
        return self.board.is_full()

    def run(self):
        while True:
            self.turn()
            terminated, winner = self.finished()
            if terminated:
                break

        if winner == self.player1_symbol:
            print("Player1 won!")
        elif winner == self.player2_symbol:
            print("Player2 won!")
        else:
            print("Draw!")
        print(self.board)

    def get_observation(self) -> np.ndarray:
        return self.board.state()

    def get_valid_actions(self) -> np.ndarray:
        vector = self.board.state().reshape(-1)
        actions = np.where(vector == 0)[0]
        return actions

    def is_valid_action(self, action: int) -> bool:
        y, x = self.to_tile(action)
        return self.board.is_empty_at(y, x)

    def check_winner(self, n: int = 3) -> int:
        """
        Checks if the board contains n-same tiles as neighbors in row, column, diagonal and anti-diagonal.

        Args:
            n (int): number of same tiles

        Returns:
            int: contains the following values:
                - self.player1_symbol: If player1 has n-same tiles (player1 wins)
                - self.player2_symbol: If player2 has n-same tiles (player2 wins)
                - 0: If nobody has n-same tiles (Draw)
        """
        if self.board.shape[0] < n and self.board.shape[1] < n:
            return 0

        # Check for rows
        for y in range(self.board.shape[0]):
            count_player1 = 0
            count_player2 = 0
            for x in range(self.board.shape[1]):
                tile = self.board.get_value_at(y, x)
                if self.player1_symbol == tile:
                    count_player1 += 1
                    count_player2 = 0
                elif self.player2_symbol == tile:
                    count_player1 = 0
                    count_player2 += 1
                else:
                    count_player1 = 0
                    count_player2 = 0

                if count_player1 >= n:
                    return self.player1_symbol
                elif count_player2 >= n:
                    return self.player2_symbol

        # Check for columns
        for x in range(self.board.shape[1]):
            count_player1 = 0
            count_player2 = 0
            for y in range(self.board.shape[0]):
                tile = self.board.get_value_at(y, x)
                if self.player1_symbol == tile:
                    count_player1 += 1
                    count_player2 = 0
                elif self.player2_symbol == tile:
                    count_player1 = 0
                    count_player2 += 1
                else:
                    count_player1 = 0
                    count_player2 = 0

                if count_player1 >= n:
                    return self.player1_symbol
                elif count_player2 >= n:
                    return self.player2_symbol

        # Check for diagonals with np.diagonal
        # See more information about diagonal in:
        # https://numpy.org/doc/stable/reference/generated/numpy.diagonal.html
        for i in range(-(self.board.shape[0] - 1), self.board.shape[1] - 1, ):
            count_player1 = 0
            count_player2 = 0
            for tile in self.board.state().diagonal(i):
                if self.player1_symbol == tile:
                    count_player1 += 1
                    count_player2 = 0
                elif self.player2_symbol == tile:
                    count_player1 = 0
                    count_player2 += 1

                if count_player1 >= n:
                    return self.player1_symbol
                elif count_player2 >= n:
                    return self.player2_symbol

        # Check for anti diagonals
        board = np.rot90(self.board.state())
        for i in range(-(board.shape[0] - 1), board.shape[1] - 1, ):
            count_player1 = 0
            count_player2 = 0
            for tile in board.diagonal(i):
                if self.player1_symbol == tile:
                    count_player1 += 1
                    count_player2 = 0
                elif self.player2_symbol == tile:
                    count_player1 = 0
                    count_player2 += 1

                if count_player1 >= n:
                    return self.player1_symbol
                elif count_player2 >= n:
                    return self.player2_symbol
        return 0

    def to_tile(self, action: int) -> tuple[int, int]:
        assert 0 <= action <= self.board.shape[0] * self.board.shape[1], "#ERROR_GAME: action is not valid!"
        y = action // self.board.shape[1]
        x = action % self.board.shape[1]
        return y, x
