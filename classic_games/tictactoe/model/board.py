import numpy as np


class TicTacToeBoard:
    def __init__(
            self,
            board: np.ndarray,
            tiles_to_win: int = 3,
            your_symbol: int = 1,
            enemy_symbol: int = -1,
            your_start: bool = True,
    ):
        """
        Args:
            board (np.ndarray): matrix of the game state
            tiles_to_win (int): number of tiles to place in row, column, diagonal, anti-diagonal to win the game
            your_symbol (int): symbol of your player
            enemy_symbol (int): symbol of enemy player
            your_start (bool): Your player starts
        """
        assert board.ndim == 2, "#ERROR_BOARD: dimension of board should be (height, width)!"
        assert board.shape[0] == board.shape[1], "#ERROR_BOARD: height and width should be the same!"
        assert board.shape[0] >= 3, "#ERROR_BOARD: height and width should be at least 3!"
        assert tiles_to_win >= 3, "#ERROR_BOARD: number of tiles to win should be at least 3!"
        assert tiles_to_win <= board.shape[0], "#ERROR_BOARD: number of tiles cannot be longer than one dimension!"
        assert your_symbol != 0 and enemy_symbol != 0, "#ERROR_BOARD: symbol of you and enemy cannot be 0!"
        assert your_symbol != enemy_symbol, "#ERROR_BOARD: symbol of you and enemy cannot be the same!"

        self._board: np.ndarray = board.copy()
        self._tiles_to_win: int = tiles_to_win
        self._your_symbol: int = your_symbol
        self._enemy_symbol: int = enemy_symbol
        self._current_player: bool = your_start
        self._winner: int = 0
        self._history: list[np.ndarray] = [self._board.copy()]

    @property
    def row(self):
        """ Returns the first dimension of the board """
        return self._board.shape[0]

    @property
    def col(self):
        """ Returns the second dimension of the board """
        return self._board.shape[1]

    def _winning_move(self, pos: tuple, your_symbol: bool) -> bool:
        """
        Checks if the given player have n tiles on the row, column, diagonal or anti-diagonal for the given position.

        Args:
            pos (tuple): position of the board (row, col)
            your_symbol (bool): Should it be checked for your player (:= True) or for the enemy (:= False).

        Returns:
            bool: True, if we have n tiles in the row, column diagonal or anti-diagonal
        """
        assert len(pos) == 2, "#ERROR_TICTACTOEBOARD: pos should be a tuple in form (row, col)!"
        assert 0 <= pos[0] < self._board.shape[0], "#ERROR_TICTACTOEBOARD: row is out of bounds!"
        assert 0 <= pos[1] < self._board.shape[1], "#ERROR_TICTACTOEBOARD: col is out of bounds!"

        row, col = pos
        symbol = self._your_symbol if your_symbol else self._enemy_symbol

        # Check for rows
        count = 0
        for c in range(self.col):
            tile = self._board[row, c]
            if tile == symbol:
                count += 1
            else:
                count = 0
            if count >= self._tiles_to_win:
                return True

        # Check for columns
        count = 0
        for r in range(self.row):
            tile = self._board[r, col]
            if tile == symbol:
                count += 1
            else:
                count = 0
            if count >= self._tiles_to_win:
                return True

        # Check for diagonals
        count = 0
        r, c = row - min(row, col), col - min(row, col)
        for i in range(min(self.row - r, self.col - c)):
            tile = self._board[r + i, c + i]
            if tile == symbol:
                count += 1
            else:
                count = 0
            if count >= self._tiles_to_win:
                return True

        # Check for anti-diagonals
        count = 0
        r, c = row - min(row, self.col - 1 - col), col + min(row, self.col - 1 - col)
        for i in range(abs(r - c) + 1):
            tile = self._board[r + i, c - i]
            if tile == symbol:
                count += 1
            else:
                count = 0
            if count >= self._tiles_to_win:
                return True
        return False

    def check_terminated(self) -> bool:
        """
        Returns True if the board is terminated state

        Returns:
            bool: True if the board is terminated state
        """
        # Check if the game is over (win or draw)
        self._winner = self.check_winner()

        # Check if the game is finished (either someone won or all tiles are placed)
        if self._winner or np.all(self._board != 0):
            return True
        return False

    def check_winner(self) -> int:
        """
        Returns the winner of the current board.

        Returns:
            int: 
                0 := no winner
                your_symbol :=  your player wins
                enemy_symbol := enemy player wins
        """
        for i in range(self.row):
            for j in range(self.col):
                if self._winning_move((i, j), your_symbol=True):
                    # Case: Your player won
                    return self._your_symbol
                elif self._winning_move((i, j), your_symbol=False):
                    # Case: Enemy player won
                    return self._enemy_symbol
        # Case: Nobody won
        return 0

    def get_current(self) -> np.ndarray:
        """
        Returns the current board state.

        Returns:
            np.ndarray: current board state
        """
        return self._board.copy()

    def get_successors(self) -> list[np.ndarray]:
        """
        Returns the successor boards, if we take an action from the current board.

        Returns:
            list[np.ndarray]: list of successor boards
        """
        successors = []
        actions = self.get_actions()
        board = self._board.copy()
        for action in actions:
            # Create the successor state
            self.set(action)

            # Append the successor state into the list of successors
            successors += [self._board.copy()]

            # Reset the board
            self._current_player = not self._current_player
            self._board = board.copy()
            self._history.pop()
        return successors

    def get_history(self) -> list[np.ndarray]:
        """
        Returns the entire history of changes on the board.

        Returns:
            list[np.ndarray]: history of changes of the board
        """
        return self._history

    def get_actions(self) -> list[int]:
        """
        Returns all possible actions of the board.

        Returns:
            list[int]: list of actions
        """
        # Get all possible actions
        board_vec = self._board.flatten()
        actions = list(np.where(board_vec == 0)[0])
        return actions

    def get_current_player(self) -> bool:
        """
        Returns the current player as bool.

        Returns:
            bool: True if your player is the current player otherwise False
        """
        return self._current_player

    def set(self, action: int):
        """
        Sets a tile on the board according to the given action.

        Args:
            action (int): Encoding of the position (n*row + col), where the tile needs to be placed
        """
        row, col = action // self.row, action % self.col
        if self._board[row, col] == 0:
            # Case: Position is empty

            if self._current_player:
                # Case: Player1 makes the move
                self._board[row, col] = self._your_symbol
            else:
                # Case: Player2 makes the move
                self._board[row, col] = self._enemy_symbol

            # Update the current player
            self._current_player = not self._current_player

            # Update the history
            self._history += [self._board.copy()]
        else:
            # Case: Position is already taken
            raise ValueError("#ERROR_TICTACTOEBOARD: action is invalid!")

    def get_reward(self) -> float:
        """
        Returns a reward of (...)
            - +1.0 if you won
            - -1.0 if enemy won
            - 0.0 if nobody won

        Returns:
            float: reward value of the current state
        """
        if self._winner == self._your_symbol:
            # Case: Player1 won the game
            # Return a reward of 1.0
            return 1.0
        elif self._winner == self._enemy_symbol:
            # Case: Player2 won the game
            # Return a reward of -1.0
            return -1.0
        elif self._winner == 0:
            # Case: Nobody won the game
            # Return a reward of 0.0
            return 0.0
        else:
            raise ValueError("#ERROR_TICTACTOEBOARD: Unknown winner state!")

    ### Feature-specific methods ###
    def get_immediate_winning_moves(self) -> int:
        """
        Returns:
            int: number of tiles, where an immediate move (next turn) refers to a win for your player.
        """
        winning_moves = 0
        for i in range(self.row):
            for j in range(self.col):
                if self._board[i, j] == 0:
                    # Case: Check if you would win if you place your symbol on this tile
                    self._board[i, j] = self._your_symbol

                    if self._winning_move((i, j), your_symbol=True):
                        # Case: Your player won
                        winning_moves += 1

                    # Reset the move
                    self._board[i, j] = 0
        return winning_moves

    def get_immediate_blocking_moves(self) -> int:
        """
        Returns:
            int: number of tiles, where an immediate move (next turn) refers to a block for a win of the enemy player.
        """
        blocking_moves = 0
        for i in range(self.row):
            for j in range(self.col):
                if self._board[i, j] == 0:
                    # Case: Check if you would win if you place your symbol on this tile
                    self._board[i, j] = self._enemy_symbol

                    if self._winning_move((i, j), your_symbol=False):
                        # Case: Enemy player won
                        blocking_moves += 1

                    # Reset the move
                    self._board[i, j] = 0
        return blocking_moves

    def __str__(self) -> str:
        return self._board.__str__()

    def __repr__(self) -> str:
        return self._board.__repr__()
