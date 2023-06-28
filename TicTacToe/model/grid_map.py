from typing import Generic, TypeVar
import numpy as np

T = TypeVar("T")


class GridMap(Generic[T]):
    """
    Creates a Grid with a shape of height x width,
    e.g. with height=3 and width=3:

    Grid map with their indices:
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

    def __init__(self, height: int, width: int, grid: np.ndarray = None):
        assert width >= 3 and height >= 3, "ERROR_GRID_MAP: width and height should be at least 3 tiles long!"
        if grid is not None:
            assert grid.shape == (height, width), "ERROR_GRID_MAP: shape of grid does not match with width and height!"
        self.width = width
        self.height = height
        self.grid = np.zeros(shape=(height, width), dtype=object) if grid is None else grid

    def set_value_at(
            self,
            y: int,
            x: int,
            val: T,
            check_range: bool = False,
            check_empty: bool = False,
    ):
        if (check_range and not self.is_valid_at(y, x)) or (check_empty and not self.is_empty_at(y, x)):
            return

        self.grid[y][x] = val

    def get_value_at(
            self,
            y: int,
            x: int,
            check_range: bool = False,
    ) -> T:
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

    def __eq__(self, other: "GridMap"):
        if isinstance(other, GridMap):
            return np.all(self.grid.__eq__(other.grid))
        elif isinstance(other, np.ndarray):
            return np.all(self.grid.__eq__(other))
        else:
            raise ValueError("ERROR_GRID_MAP: type of other should be GridMap or np.ndarray!")

    def __str__(self):
        return self.grid.__str__()
