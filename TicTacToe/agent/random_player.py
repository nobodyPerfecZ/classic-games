import numpy as np

from TicTacToe.agent.abstract_player import Player
from TicTacToe.game.abstract_game import Game
from TicTacToe.model.board import Board


class RandomPlayer(Player):

    def __init__(self, player_name: str = "Random Player", seed: int = None):
        self.player_name = player_name
        self.seed = seed
        if seed is not None:
            np.random.seed(seed=self.seed)

    @property
    def name(self) -> str:
        return self.player_name

    def start(self, turn: int, game: Game, symbol: int) -> int:
        return self.act(turn, game, symbol)

    def act(self, turn: int, game: Game, symbol: int) -> int:
        actions = game.get_valid_actions()
        return np.random.choice(actions)

    def end(self, turn: int, board: Board, symbol: int) -> int:
        pass
