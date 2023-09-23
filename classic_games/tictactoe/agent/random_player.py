import numpy as np

from typing import Optional
from gymnasium.core import ObsType
from classic_games.tictactoe.agent.abstract_player import Player
from classic_games.tictactoe.model.boardC import TicTacToeBoardC


class RandomPlayer(Player):

    def __init__(
            self,
            your_symbol: int,
            enemy_symbol: int,
            tiles_to_win: int,
            player_name: str = "Random Player",
            seed: Optional[int] = None
    ):
        super().__init__(your_symbol, enemy_symbol, tiles_to_win, player_name, seed)

    def start(self, board: ObsType) -> int:
        # Update turns
        self._turn += 1

        # Get all valid actions
        state = TicTacToeBoardC(
            board=board,
            your_symbol=self._your_symbol,
            enemy_symbol=self._enemy_symbol,
            tiles_to_win=self._tiles_to_win,
            your_start=True,
        )
        actions = state.get_actions()
        return np.random.choice(actions)

    def act(self, board: ObsType) -> int:
        if self._turn == 0:
            # Case: First move to take
            return self.start(board)
        else:
            # Case: 2, ..., n move to take

            # Update turns
            self._turn += 1

            # Get all valid actions
            state = TicTacToeBoardC(board)
            actions = state.get_actions()
            return np.random.choice(actions)

    def end(self, board: ObsType) -> int:
        pass
