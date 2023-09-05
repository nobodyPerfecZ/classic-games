from typing import Optional
from gymnasium.core import ObsType

from classic_games.tictactoe.agent.abstract_player import Player


class HumanPlayer(Player):

    def __init__(
            self,
            your_symbol: int,
            enemy_symbol: int,
            tiles_to_win: int,
            player_name: str = "Human Player",
            seed: Optional[int] = None
    ):
        super().__init__(your_symbol, enemy_symbol, tiles_to_win, player_name, seed)

    def start(self, board: ObsType) -> int:
        # TODO: Implement here
        pass

    def act(self, board: ObsType) -> int:
        # TODO: Implement here
        if self._turn == 0:
            return self.start(board)
        else:
            pass

    def end(self, board: ObsType) -> int:
        # TODO: Implement here
        pass

