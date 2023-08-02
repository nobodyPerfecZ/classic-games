import numpy as np


class RuleSettings:

    def __init__(
            self,
            board_shape: tuple[int, int],
            tiles_to_win: int,
            your_symbol: int,
            enemy_symbol: int,
    ):
        """
        Args:
            board_shape (tuple[int, int]): shape of the matrix
            tiles_to_win (int): number of tiles to place in row, column, diagonal, anti-diagonal to win the game. Defaults to 3.
            your_symbol (int): symbol of your player. Defaults to 1.
            enemy_symbol (int): symbol of enemy player. Defaults to -1
        """
        self.board_shape = board_shape
        self.tiles_to_win = tiles_to_win
        self.your_symbol = your_symbol
        self.enemy_symbol = enemy_symbol

    def export(self) -> dict:
        """
        Returns the RuleSettings as a dictionary.

        Returns:
            dict: dictionary representation of the RuleSettings
        """
        return {
            "board_shape": self.board_shape,
            "tiles_to_win": self.tiles_to_win,
            "your_symbol": self.your_symbol,
            "enemy_symbol": self.enemy_symbol,
        }

