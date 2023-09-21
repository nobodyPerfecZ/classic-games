import numpy as np
import ctypes

TicTacToe_lib = ctypes.CDLL(r"./classic_games/tictactoe/model/board.dll")


class TicTacToeBoardC:
    def __init__(self,
                 board: np.ndarray,
                 tiles_to_win: int = 3,
                 your_symbol: int = 1,
                 enemy_symbol: int = -1,
                 your_start: bool = True
                 ):
        """
        Args:
            board (np.ndarray): matrix of the game state
            tiles_to_win (int): number of tiles to place in row, column, diagonal, anti-diagonal to win the game.
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

        # Define argument and return types for the functions
        TicTacToe_lib.create_TicTacToeBoard.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int,
                                                        ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_bool]
        TicTacToe_lib.create_TicTacToeBoard.restype = ctypes.POINTER(ctypes.c_void_p)

        TicTacToe_lib.row.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.row.restype = ctypes.c_int

        TicTacToe_lib.col.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.col.restype = ctypes.c_int

        TicTacToe_lib.check_terminated.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.check_terminated.restype = ctypes.c_bool

        TicTacToe_lib.check_winner.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.check_winner.restype = ctypes.c_int

        TicTacToe_lib.get_current.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.get_current.restype = ctypes.POINTER(ctypes.c_int)

        TicTacToe_lib.get_successors_length.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.get_successors_length.restype = ctypes.c_int

        TicTacToe_lib.get_successors.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.get_successors.restype = ctypes.POINTER(ctypes.c_int)

        TicTacToe_lib.get_history_length.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.get_history_length.restype = ctypes.c_int

        TicTacToe_lib.get_history.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.get_history.restype = ctypes.POINTER(ctypes.c_int)

        TicTacToe_lib.get_actions_length.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.get_actions_length.restype = ctypes.c_int

        TicTacToe_lib.get_actions.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.get_actions.restype = ctypes.POINTER(ctypes.c_int)

        TicTacToe_lib.get_current_player.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.get_current_player.restype = ctypes.c_bool

        TicTacToe_lib.set.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_int]
        TicTacToe_lib.set.restype = None

        TicTacToe_lib.get_reward.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.get_reward.restype = ctypes.c_float

        TicTacToe_lib.get_immediate_winning_moves.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.get_immediate_winning_moves.restype = ctypes.c_int

        TicTacToe_lib.get_immediate_blocking_moves.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        TicTacToe_lib.get_immediate_blocking_moves.restype = ctypes.c_int

        # Create the TicTacToeBoard object
        row, col = board.shape
        c_array = board.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        self.obj = TicTacToe_lib.create_TicTacToeBoard(c_array, row, col, tiles_to_win, your_symbol, enemy_symbol,
                                                       your_start)

    @property
    def row(self) -> int:
        return TicTacToe_lib.row(self.obj)

    @property
    def col(self) -> int:
        return TicTacToe_lib.col(self.obj)

    def check_terminated(self) -> bool:
        """
        Returns True if the board is terminated state

        Returns:
            bool: True if the board is terminated state
        """
        return TicTacToe_lib.check_terminated(self.obj)

    def check_winner(self) -> int:
        """
        Returns the winner of the current board.

        Returns:
            int: 0 - no winner, your_symbol - your player wins, enemy_symbol - enemy player wins
        """
        return TicTacToe_lib.check_winner(self.obj)

    def get_current(self) -> np.ndarray:
        """
        Returns the current board state.

        Returns:
            np.ndarray: current board state
        """
        c_board = TicTacToe_lib.get_current(self.obj)
        length = self.row * self.col

        # Convert C array to a numpy array
        board = [c_board[i] for i in range(length)]
        board = np.array(board, dtype=np.int32).reshape((self.row, self.col))

        # Free allocated memory
        TicTacToe_lib.delete_vector(c_board)

        return board

    def get_successors(self) -> list[np.ndarray]:
        """
        Returns the successor boards, if we take an action from the current board.

        Returns:
            list[np.ndarray]: list of successor boards
        """
        c_list_boards = TicTacToe_lib.get_successors(self.obj)
        length = TicTacToe_lib.get_successors_length(self.obj)

        # Convert C array to a list of np.ndarrays
        history = []

        for i in range(length):
            board = [c_list_boards[i * (self.row * self.col) + j] for j in range(self.row * self.col)]
            board = np.array(board, dtype=np.int32).reshape((self.row, self.col))
            history.append(board)

        # Free allocated memory
        TicTacToe_lib.delete_vector(c_list_boards)
        return history

    def get_history(self) -> list[np.ndarray]:
        """
        Returns the entire history of changes on the board.

        Returns:
            list[np.ndarray]: history of changes of the board
        """
        c_list_boards = TicTacToe_lib.get_history(self.obj)
        length = TicTacToe_lib.get_history_length(self.obj)

        # Convert C array to a list of np.ndarrays
        history = []

        for i in range(length):
            board = [c_list_boards[i * (self.row * self.col) + j] for j in range(self.row * self.col)]
            board = np.array(board, dtype=np.int32).reshape((self.row, self.col))
            history.append(board)

        # Free allocated memory
        TicTacToe_lib.delete_vector(c_list_boards)
        return history

    def get_actions(self) -> list[int]:
        """
        Returns all possible actions of the board.

        Returns:
            list[int]: list of actions
        """
        c_actions = TicTacToe_lib.get_actions(self.obj)
        length = TicTacToe_lib.get_actions_length(self.obj)

        # Convert C array to a python list
        actions = [c_actions[i] for i in range(length)]

        # Free allocated memory
        TicTacToe_lib.delete_vector(c_actions)

        return actions

    def get_current_player(self) -> bool:
        """
        Returns the current player as bool.

        Returns:
            bool: True if your player is the current player otherwise False
        """
        return TicTacToe_lib.get_current_player(self.obj)

    def set(self, action: int) -> None:
        """
        Sets a tile on the board according to the given action.

        Args:
            action (int): Encoding of the position (n*row + col), where the tile needs to be placed
        """
        TicTacToe_lib.set(self.obj, action)

    def get_reward(self) -> float:
        """
        Returns a reward of (...)
            - +1.0 if you won
            - -1.0 if enemy won
            - 0.0 if nobody won

        Returns:
            float: reward value of the current state
        """
        return TicTacToe_lib.get_reward(self.obj)

    def get_immediate_winning_moves(self) -> int:
        """
        Returns:
            int: number of tiles, where an immediate move (next turn) refers to a win for your player.
        """
        return TicTacToe_lib.get_immediate_winning_moves(self.obj)

    def get_immediate_blocking_moves(self) -> int:
        """
        Returns:
            int: number of tiles, where an immediate move (next turn) refers to a block for a win of the enemy player.
        """
        return TicTacToe_lib.get_immediate_blocking_moves(self.obj)
