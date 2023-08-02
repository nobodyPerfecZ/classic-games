from abc import ABC, abstractmethod
from typing import Optional
from gymnasium.core import ObsType
import numpy as np


class Player(ABC):
    """
    This class represents a general player for the tictactoe Environment,
    where the player decides its action based on the observation
    that he gets.

    The observation of the tictactoe environment is a matrix, where (...):
    - tiles of player1 (you/your agent) are represented as your_symbol (default: +1)
    - tiles of player2 (enemy agent) are represented as enemy_symbol (default: -1)
    The following example shows the observation of a 3x3 tictactoe board:
    [
    [0, 1, 1],
    [-1 0, 0],
    [-1, 0, 0],
    ]
    """

    def __init__(
            self,
            your_symbol: int,
            enemy_symbol: int,
            tiles_to_win: int,
            player_name: str,
            seed: Optional[int] = None
    ):
        """
        Args:
            your_symbol (int): symbol of your player
            enemy_symbol (int): symbol of enemy player
            tiles_to_win (int): number of tiles to be in row/col/diagonal/anti-diagonal to win the game
            player_name (str): name of the player
            seed (Optional[int]): seed for the random number generator. Defaults to None
        """
        self._your_symbol: int = your_symbol
        self._enemy_symbol: int = enemy_symbol
        self._tiles_to_win: int = tiles_to_win
        self._player_name: str = player_name
        self._np_random: int = seed
        self._turn: int = 0

        # Sets the seed
        self._seed(seed=self._np_random)

    @property
    def name(self) -> str:
        """
        Returns the name of the player

        Returns:
            str: name of the player
        """
        return self._player_name

    def _seed(self, seed: Optional[int] = None):
        """
        Sets the random seed for the player.
        This function is only called for reset() and __init__().

        Args:
            seed (Optional[int]): seed for the random number generator. Defaults to None
        """
        self._np_random = seed
        np.random.seed(seed=self._np_random)

    def reset(self, seed: Optional[int] = None):
        """
        Resets the agent with the given random number seed.

        Args:
            seed (Optional[int]): seed for the random number generator. Defaults to None.
        """
        self._turn = 0  # set the number of turns to 0
        self._seed(seed)  # set the random number to the given seed

    @abstractmethod
    def start(self, board: ObsType) -> int:
        """
        First move to take.

        Args:
            board (ObsType): current observation (board state)

        Returns:
            int: action to take
        """
        pass

    @abstractmethod
    def act(self, board: ObsType) -> int:
        """
        Returns the action of the player for the 2, ..., n turns.

        Args:
            board (ObsType): current observation (board state)

        Returns:
            int: action to take
        """
        pass

    @abstractmethod
    def end(self, board: ObsType) -> int:
        """
        Returns the action of the player after the last turn.

        Args:
            board (ObsType): current observation (board state)

        Returns:
            int: action to take
        """
        pass
