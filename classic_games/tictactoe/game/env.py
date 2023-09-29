from math import prod
from typing import Optional

import gymnasium as gym
import numpy as np
from gymnasium.spaces import Discrete, Box

from classic_games.tictactoe.agent.abstract_player import Player
from classic_games.tictactoe.agent.random_player import RandomPlayer
from classic_games.tictactoe.model.board import TicTacToeBoard
from classic_games.tictactoe.model.render import TicTacToeRender
from classic_games.tictactoe.model.metadata import Metadata


class TicTacToeEnv(gym.Env):
    """ Represents the TicTacToe game as a gymnasium environment object. """
    # Has to be here so that we do not get any errors in the console
    metadata: dict = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 30,
    }

    def __init__(
            self,
            rule_settings: Metadata = Metadata(),
            enemy_player: Player = RandomPlayer(your_symbol=-1,
                                                enemy_symbol=1,
                                                tiles_to_win=3),
            seed: Optional[int] = None,
            render_mode: Optional[str] = None,
    ):
        """
        Args:
            rule_settings (Metadata): contains meta information about the TicTacToe Environment
            enemy_player (Player): enemy player
            seed (int): seed for the random number generator
            render_mode (str): mode to render the environment
        """
        super(TicTacToeEnv, self).__init__()

        # Safe the rule settings
        self._rule_settings = rule_settings
        TicTacToeEnv.metadata = self._rule_settings.to_dict()

        self._render = TicTacToeRender(
            window_shape=(400, 600),
            board_shape=self._rule_settings.board_shape,
            mode=render_mode,
            your_symbol=self._rule_settings.your_symbol,
            enemy_symbol=self._rule_settings.enemy_symbol,
        )

        # Define the action and observation space
        # n*m - 1 possible positions on the board. E.g.: (3x3) -> (0, 1, ..., 8)
        self.action_space = Discrete(prod(self._rule_settings.board_shape) - 1)
        self.observation_space = Box(
            low=self._rule_settings.enemy_symbol,
            high=self._rule_settings.your_symbol,
            shape=self._rule_settings.board_shape,
            dtype=np.int32,
        )
        self._render_mode = render_mode

        # Create enemy player (seeds are placed later on)
        self._enemy_player = enemy_player

        # Set the seeds of the environment and the player
        self._np_random = seed
        self._seed(seed)

        # Create the environment
        self._board = TicTacToeBoard(
            board=np.zeros(shape=self._rule_settings.board_shape, dtype=np.int32),
            tiles_to_win=self._rule_settings.tiles_to_win,
            your_symbol=self._rule_settings.your_symbol,
            enemy_symbol=self._rule_settings.enemy_symbol,
            your_start=np.random.choice([True, False]),
        )
        self._terminated = False
        self._truncated = False
        self._last_render = False  # control variable to render the last frame

        # Do the first move if enemy starts with the game
        if not self._board.get_current_player():
            # Case: player2 starts the game
            action = self._enemy_player.act(self._board.get_current())
            self._board.set(action)

    def _seed(self, seed: Optional[int] = None):
        """
        Sets the random seed for the environment and the enemy player.

        Args:
            seed (int): seed for the random number generator
        """
        self._np_random = seed
        np.random.seed(self._np_random)
        self._enemy_player.reset(self._np_random)

    def reset(self, seed: Optional[int] = None, options: Optional[dict[str]] = None):
        # Reset the seed
        self._seed(seed)

        # Reset the board
        self._board = TicTacToeBoard(
            board=np.zeros(shape=self._rule_settings.board_shape, dtype=np.int32),
            tiles_to_win=self._rule_settings.tiles_to_win,
            your_symbol=self._rule_settings.your_symbol,
            enemy_symbol=self._rule_settings.enemy_symbol,
            your_start=np.random.choice([True, False]),
        )
        self._terminated = False
        self._truncated = False
        self._last_render = False

        # Do the first move if the enemy starts first
        if not self._board.get_current_player():
            # Case: player2 starts the game
            action = self._enemy_player.act(self._board.get_current())
            self._board.set(action)
        return self._board.get_current(), TicTacToeEnv.metadata

    def step(self, action: int):
        if self._terminated:
            # Case: Game is already finished
            # Do no step anymore
            return self._board.get_current(), self._board.get_reward(), self._terminated, self._truncated, \
                   TicTacToeEnv.metadata

        # Do the action and check if the game is terminated
        self._board.set(action)
        self._terminated = self._board.check_terminated()

        if self._terminated:
            # Case: Game is finished after the last move
            # Do no step anymore
            return self._board.get_current(), self._board.get_reward(), self._terminated, self._truncated, \
                   TicTacToeEnv.metadata

        if not self._board.get_current_player():
            # Case: Next player is enemy
            action = self._enemy_player.act(self._board.get_current())

            # Do the action
            self._board.set(action)

            # Check if board is now terminated
            self._terminated = self._board.check_terminated()

        return self._board.get_current(), self._board.get_reward(), self._terminated, self._truncated,\
            TicTacToeEnv.metadata

    def render(self):
        if self._render_mode == "human":
            if self._rule_settings.board_shape[0] > 4 and self._rule_settings.board_shape[1] > 4:
                raise ValueError("#ERROR_ENV: You can only render the board with a shape of maximal (4, 4)!")
            if not self._last_render:
                if self._terminated:
                    self._last_render = True
                self._render.init()
                self._render.draw_step(self._board.get_history())
        elif self._render_mode == "rgb_array":
            self._render.init()
            return self._render.get_rgb_array(self._board.get_current())

    def close(self):
        self._render.close()
