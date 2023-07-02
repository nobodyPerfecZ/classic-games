from abc import ABC, abstractmethod

from TicTacToe.game.abstract_game import Game
from TicTacToe.model.board import Board


class Player(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Returns the name of the player

        Returns:
            str: name of the player
        """

    @abstractmethod
    def start(self, turn: int, game: Game, symbol: int) -> int:
        """
        First move to take.

        Args:
            turn (int): current turn
            game (Game): game object with the current state
            symbol (int): symbol of the player

        Returns:
            int: action to take
        """
        pass

    @abstractmethod
    def act(self, turn: int, game: Game, symbol: int) -> int:
        """
        Returns the action of the player for the 2, ..., n turns.

        Args:
            turn (int): current turn
            game (Game): game object with the current state
            symbol (int): symbol of the player

        Returns:
            int: action to take
        """
        pass

    @abstractmethod
    def end(self, turn: int, game: Game, symbol: int) -> int:
        """
        Returns the action of the player after the last turn.

        Args:
            turn (int): current turn
            game (Game): game object with the current state
            symbol (int): symbol of the player

        Returns:
            int: action to take
        """
        pass
