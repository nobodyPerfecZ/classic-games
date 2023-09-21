from typing import Optional
from gymnasium.core import ObsType
import numpy as np
import ctypes
import os

from classic_games.tictactoe.agent.abstract_player import Player

MiniMax_lib = ctypes.CDLL(os.path.join(os.getcwd(), r"./classic_games/tictactoe/agent/min_max.dll"))


class MiniMaxC:
    def __init__(self, your_symbol: int, enemy_symbol: int, tiles_to_win: int, max_depth: int = np.iinfo(np.int32).max):
        """
        Args:
            your_symbol (int): symbol of your player
            enemy_symbol (int): symbol of enemy player
            tiles_to_win (int): number of tiles to be in row/col/diagonal/anti-diagonal to win the game
            max_depth (int): maximal depth for the minimax algorithm
        """
        assert max_depth >= 1, "#ERROR_MINIMAXC: max_depth should be higher or equal to 1!"

        # Define argument and return types for the functions
        MiniMax_lib.create_MiniMax.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        MiniMax_lib.create_MiniMax.restype = ctypes.POINTER(ctypes.c_void_p)

        MiniMax_lib.get_best_action.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_int),
                                                ctypes.c_int, ctypes.c_int]
        MiniMax_lib.get_best_action.restype = ctypes.c_int

        self.obj = MiniMax_lib.create_MiniMax(your_symbol, enemy_symbol, tiles_to_win, max_depth)

    def get_best_action(self, board: ObsType):
        """
        Returns the best action from the given state, according to the MiniMax algorithm.

        Args:
            board (ObsType): current state

        Returns:
            int: best action with the given state
        """
        row, col = board.shape
        # board = board.astype(np.int32)
        c_array = board.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        return MiniMax_lib.get_best_action(self.obj, c_array, row, col)


class MinMaxPlayerC(Player):
    """
    Represents a player which uses the Min-Max algorithm
    with alpha-beta pruning to decide the next action.
    """

    def __init__(
            self,
            your_symbol: int,
            enemy_symbol: int,
            tiles_to_win: int,
            player_name: str = "MinMax Player",
            seed: Optional[int] = None,
            max_depth: int = np.iinfo(np.int32).max,
    ):
        super().__init__(your_symbol, enemy_symbol, tiles_to_win, player_name, seed)
        self._minimaxC = MiniMaxC(
            your_symbol=your_symbol,
            enemy_symbol=enemy_symbol,
            tiles_to_win=tiles_to_win,
            max_depth=max_depth
        )

    def start(self, board: ObsType) -> int:
        # Update turn
        self._turn += 1

        # Get the (best) action from minimax algorithm
        action = self._minimaxC.get_best_action(board)
        return action

    def act(self, board: ObsType) -> int:
        if self._turn == 0:
            return self.start(board)
        else:
            # Update turn
            self._turn += 1

            # Get the (best) action from minimax algorithm
            action = self._minimaxC.get_best_action(board)
            return action

    def end(self, board: ObsType) -> int:
        pass
