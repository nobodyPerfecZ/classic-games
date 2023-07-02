from abc import ABC, abstractmethod

import numpy as np


class Game(ABC):

    @property
    @abstractmethod
    def observation_space(self) -> np.ndarray:
        """
        Returns:
            np.ndarray: shape of the observation space
        """
        pass

    @property
    @abstractmethod
    def action_space(self) -> np.ndarray:
        """
        Returns:
            np.ndarray: shape of the action space
        """
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def turn(self):
        pass

    @abstractmethod
    def finished(self):
        pass

    @abstractmethod
    def terminated(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def get_observation(self):
        pass

    @abstractmethod
    def get_valid_actions(self):
        pass

    @abstractmethod
    def is_valid_action(self):
        pass
