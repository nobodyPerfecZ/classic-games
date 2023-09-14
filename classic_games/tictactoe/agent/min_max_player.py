from typing import Optional

import numpy as np
from gymnasium.core import ObsType

from classic_games.tictactoe.agent.abstract_player import Player
from classic_games.tictactoe.model.board import TicTacToeBoard


class MiniMax:
    """
    Implements the Mini-Max algorithm with alpha/beta pruning.
    """

    # TODO: Implement MinMax Algorithm in C++ (to make it much faster!!!)

    def __init__(self, your_symbol: int, enemy_symbol: int, tiles_to_win: int):
        """
        Args:
            your_symbol (int):
                symbol of your player
            enemy_symbol (int):
                symbol of enemy player
            tiles_to_win (int):
                number of tiles to be in row/col/diagonal/anti-diagonal to win the game
        """
        # cache variable to safe for each hash(state) := (reward, best action)
        self._cache: dict[str, tuple[float, int]] = {}
        self._your_start: bool = True
        self._depth: int = 0
        self._alpha: float = -np.inf
        self._beta: float = np.inf
        self._your_symbol: int = your_symbol
        self._enemy_symbol: int = enemy_symbol
        self._tiles_to_win: int = tiles_to_win

    def _reset(self):
        """
        Resets the parameters of the minimax-search.
        """
        self._your_start = True
        self._depth = 0
        self._alpha = -np.inf
        self._beta = np.inf

    def get_best_action(self, board: ObsType) -> int:
        """
        Returns the best action from the given state, according to the MiniMax algorithm.

        Args:
            board (ObsType):
                current state

        Returns:
            int: best action with the given state
        """
        # Create the hash value
        hash_value = board.tobytes()
        if hash_value in self._cache:
            # Case: Already used minimax algorithm for that state
            return self._cache[hash_value][1]

        # Reset the parameters
        self._reset()

        # Perform the minimax algorithm (with alpha-beta pruning)
        reward, action = self._minimax(board)

        # Safe (reward, action) to the cache
        self._cache[hash_value] = reward, action
        return action

    def _minimax(self, board: ObsType) -> tuple:
        """
        The upper part from the Minimax algorithm, where we return the (reward, action)
        pair of a given state. If the state is non-terminated then go deeper in the tree.

        Args:
            board (ObsType):
                current state

        Returns:
            tuple: (reward, action) pair of the current state
        """
        state = TicTacToeBoard(
            board=board,
            your_symbol=self._your_symbol,
            enemy_symbol=self._enemy_symbol,
            tiles_to_win=self._tiles_to_win,
            your_start=self._your_start
        )

        if state.check_terminated():
            reward = state.get_reward() * (2 * (board.shape[0] * board.shape[1]) - self._depth)
            return reward, -1  # (reward, action)
        elif self._your_start:
            # Case: Max player makes a turn
            return self._max(board)
        else:
            # Case: Min player makes a turn
            return self._min(board)

    def _max(self, board: ObsType) -> tuple:
        """
        The max-part of the Minimax algorithm. It returns
        the (reward, action) pair of a given state, so that
        we maximize our reward.

        Args:
            board (ObsType):
                current state

        Returns:
            tuple: (reward, action) pair which maximizes our reward from the given state
        """
        state = TicTacToeBoard(
            board=board,
            your_symbol=self._your_symbol,
            enemy_symbol=self._enemy_symbol,
            tiles_to_win=self._tiles_to_win,
            your_start=True,
        )
        best_v = -np.inf, -1

        # Safe the old parameters
        cur_depth = self._depth
        cur_alpha = self._alpha

        for successor, action in zip(state.get_successors(), state.get_actions()):
            # Update the parameters
            self._depth = cur_depth + 1
            self._your_start = False

            v = self._minimax(successor)
            if v[0] > best_v[0]:
                best_v = v[0], action
            if best_v[0] >= self._beta:
                self._alpha = cur_alpha
                return best_v
            self._alpha = max(self._alpha, best_v[0])
        self._alpha = cur_alpha
        return best_v

    def _min(self, board: ObsType) -> tuple:
        """
        The min-part of the Minimax algorithm. It returns
        the (reward, action) pair of a given state, so that
        we minimize our reward.

        Args:
            board (ObsType):
                current state

        Returns:
            tuple: (reward, action) pair which minimize our reward from the given state
        """
        state = TicTacToeBoard(
            board=board,
            your_symbol=self._your_symbol,
            enemy_symbol=self._enemy_symbol,
            tiles_to_win=self._tiles_to_win,
            your_start=False,
        )
        best_v = np.inf, -1

        # Safe the old parameters
        cur_depth = self._depth
        cur_beta = self._beta

        for successor, action in zip(state.get_successors(), state.get_actions()):
            # Update the parameters
            self._depth = cur_depth + 1
            self._your_start = True

            v = self._minimax(successor)
            if v[0] < best_v[0]:
                best_v = v[0], action
            if best_v[0] <= self._alpha:
                self._beta = cur_beta
                return best_v
            self._beta = min(self._beta, best_v[0])
        self._beta = cur_beta
        return best_v


class MinMaxPlayer(Player):
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
            seed: Optional[int] = None
    ):
        super().__init__(your_symbol, enemy_symbol, tiles_to_win, player_name, seed)
        self._minimax = MiniMax(
            your_symbol=your_symbol,
            enemy_symbol=enemy_symbol,
            tiles_to_win=tiles_to_win
        )

    def start(self, board: ObsType) -> int:
        # Update turn
        self._turn += 1

        # Get the (best) action from minimax algorithm
        return self._minimax.get_best_action(board)

    def act(self, board: ObsType) -> int:
        if self._turn == 0:
            return self.start(board)
        else:
            # Update turn
            self._turn += 1

            # Get the (best) action from minimax algorithm
            return self._minimax.get_best_action(board)

    def end(self, board: ObsType) -> int:
        pass
