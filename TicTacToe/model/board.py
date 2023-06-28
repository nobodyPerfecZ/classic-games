import copy
import json
from typing import TypeVar

import numpy as np

from TicTacToe.model.grid_map import GridMap

T = TypeVar("T")


class Board(GridMap[T]):
    def __init__(
            self,
            height: int,
            width: int,
            turn: int = 0,
            grid: np.ndarray = None,
            history: list[np.ndarray] = None,
    ):
        super().__init__(height, width, grid)
        self.turn = turn
        self.history = history if history else []

    def set_value_at(
            self,
            y: int,
            x: int,
            val: T,
            check_range: bool = False,
            check_empty: bool = False,
    ):
        self.history += [copy.deepcopy(self.grid)]
        self.turn += 1
        super().set_value_at(y, x, val, check_range, check_empty)

    def save_board(self, name: str):
        state = {
            "grid": self.grid.tolist(),
            "history": [grid.tolist() for grid in self.history],
            "turn": self.turn,
        }
        with open(f"{name}.json", "w") as file_object:
            json.dump(state, file_object)

    @staticmethod
    def load_board(name: str) -> "Board":
        with open(f"{name}.json", "r") as file_object:
            data = json.load(file_object)

        # Convert list to np.ndarray
        grid = np.array(data["grid"])

        # Convert list to np.ndarray
        history = [np.array(list(map(int, grid))) for grid in data["history"]]

        turn = data["turn"]
        return Board(grid.shape[0], grid.shape[1], turn, grid, history)

    def __eq__(self, other: "Board"):
        if isinstance(other, Board):
            return self.turn.__eq__(other.turn) and \
                np.all(self.history.__eq__(other.history)) and \
                super().__eq__(other)
        else:
            raise ValueError("ERROR_BOARD: type of other should be Board!")

    def __str__(self):
        text = ""
        text += f"turn: {self.turn}\n"
        text += f"board: {self.grid}"
        return text
