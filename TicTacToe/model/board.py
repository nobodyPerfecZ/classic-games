import copy
import json
from typing import Union

import numpy as np


class Board:
    """
        Creates a Grid with a shape of (height, width),
        e.g. Board with (height=3, width=3) and their indices:
        |(0,0)|(0,1)|(0,2)|
        |(1,0)|(1,1)|(1,2)|
        |(2,0)|(2,1)|(2,2)|

        Args:
            height (int): number of tiles on the y-axis
            width (int): number of tiles on the x-axis
            grid (np.ndarray, optional):
                grid representation as numpy array of shape (height, width).
                The shape should be equal to given width and height.
        """

    def __init__(
            self,
            height: int = None,
            width: int = None,
            grid: np.ndarray = None,
            history: list[np.ndarray] = None,
    ):
        if height is not None and width is not None:
            # Case: Height and width are given
            assert width >= 3 and height >= 3, "#ERROR_GRID_MAP: width and height should be at least 3 tiles long!"
            self.height = height
            self.width = width
            if grid is not None:
                # Case: Height, width and grid are given
                assert grid.shape == (height, width), \
                    "ERROR_GRID_MAP: shape of grid does not match with width and height!"
                self.grid = grid
            else:
                # Case: Height and width but no grid are given
                self.grid = np.zeros(shape=(height, width), dtype=int)
        elif grid is not None:
            # Case: Only grid are given
            self.height = grid.shape[0]
            self.width = grid.shape[1]
            self.grid = grid
        self.history = history if history else []

    @property
    def shape(self) -> tuple[int, int]:
        return self.grid.shape

    @property
    def total_history(self) -> list[np.ndarray]:
        return self.history + [copy.deepcopy(self.grid)]

    def state(self, n: int = 0) -> np.ndarray:
        assert 0 <= n < len(self.history) + 1, \
            f"ERROR_BOARD: n should be in between 0 (inclusive) and {len(self.history) + 1} (exclusive)!"
        if n != 0:
            # Case: Check in history for the previous state
            return self.history[-n]
        else:
            # Case: Return the current state
            return self.grid

    def set_value_at(
            self,
            y: int,
            x: int,
            val: int,
            check_range: bool = False,
            check_empty: bool = False,
    ):
        if (check_range and not self.is_valid_at(y, x)) or (check_empty and not self.is_empty_at(y, x)):
            return

        # Update the history
        self.history += [copy.deepcopy(self.grid)]
        self.grid[y][x] = val

    def get_value_at(self, y: int, x: int, check_range: bool = False) -> int:
        if check_range and not self.is_valid_at(y, x):
            return
        return self.grid[y][x]

    def is_valid_at(self, y: int, x: int) -> bool:
        if 0 <= y < self.height and 0 <= x < self.width:
            return True
        return False

    def is_empty_at(self, y: int, x: int, check_range: bool = False) -> bool:
        if check_range and not self.is_valid_at(y, x):
            return

        if self.grid[y][x] == 0:
            return True
        return False

    def is_full(self) -> bool:
        return np.all(self.grid != 0)

    def save_board(self, name: str):
        state = {
            "grid": self.grid.tolist(),
            "history": [grid.tolist() for grid in self.history],
        }
        with open(f"{name}.json", "w") as file_object:
            json.dump(state, file_object)

    @staticmethod
    def load_board(name: str) -> "Board":
        with open(f"{name}.json", "r") as file_object:
            data = json.load(file_object)

        # Convert current state (grid) to np.ndarray
        grid = np.array(data["grid"], dtype=int)

        # Convert history to np.ndarray
        history = [np.array(grid, dtype=int) for grid in data["history"]]

        return Board(height=None, width=None, grid=grid, history=history)

    def __eq__(self, other: Union["Board", np.ndarray]):
        if isinstance(other, Board):
            return np.all(self.history.__eq__(other.history)) and \
                np.all(self.grid.__eq__(other.grid)) and \
                (self.height == other.height) and \
                (self.width == other.width)
        elif isinstance(other, np.ndarray):
            return np.all(self.grid.__eq__(other))
        else:
            raise ValueError("ERROR_BOARD: type of other should be Board or np.ndarray!")

    def __str__(self):
        return self.grid.__str__()
