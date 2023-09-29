from typing import Optional
from gymnasium.core import ObsType
import numpy as np

from classic_games.tictactoe.agent.abstract_player import Player
from classic_games.tictactoe.agent.min_max import MiniMax


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
            seed: Optional[int] = None,
            max_depth: int = np.iinfo(np.int32).max,
    ):
        super().__init__(your_symbol, enemy_symbol, tiles_to_win, player_name, seed)
        self._minimaxC = MiniMax(
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
