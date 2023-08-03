from typing import Union

import numpy as np
import pygame


class TicTacToeRender:

    def __init__(
            self,
            window_shape: tuple[int, int],  # in (H, W) format
            board_shape: tuple[int, int],  # in (H, W) format
            mode: str,  # either "human" or "rgb_array"
            your_symbol: int,
            enemy_symbol: int,
            your_color: tuple[int, int, int] = (0, 128, 0),  # in (R, G, B) format
            enemy_color: tuple[int, int, int] = (255, 0, 0),  # in (R, G, B) format
            caption: str = "TicTacToe-v0",
    ):
        """
        Args:
            window_shape (tuple[int, int]): shape of the pygame window/rgb-array in (H, W) format
            board_shape (tuple[int, int]): shape of the tictactoe board in (H, W) format
            mode (str): render mode. Can be either "human" or "rgb_array"
            your_symbol (int): symbol of your player
            enemy_symbol (int): symbol of enemy player
            your_color (tuple[int, int, int]): color of your player symbol
            enemy_color (tuple[int, int, int]): color of enemy player symbol
            caption (str): caption of the pygame window
        """
        self._window_shape: tuple[int, int] = window_shape
        self._board_shape: tuple[int, int] = board_shape
        self._mode: str = mode
        self._your_symbol: int = your_symbol
        self._enemy_symbol: int = enemy_symbol
        self._your_color: int = your_color
        self._enemy_color: int = enemy_color
        self._caption: str = caption

        self._screen: Union[pygame.display, pygame.Surface] = None
        self._clock: pygame.time.Clock = None
        self._font: pygame.font = None

    @property
    def window_height(self) -> int:
        return self._window_shape[0]

    @property
    def window_width(self) -> int:
        return self._window_shape[1]

    @property
    def board_height(self) -> int:
        return self._board_shape[0]

    @property
    def board_width(self) -> int:
        return self._board_shape[1]

    def init(self):
        """
        Initialize the pygame objects, to render the frames.
        """
        pygame.init()
        pygame.display.set_caption(self._caption)

        if self._mode == "human":
            self._screen = pygame.display.set_mode((self.window_width, self.window_height))
        elif self._mode == "rgb_array":
            self._screen = pygame.Surface((self.window_width, self.window_height))
        else:
            raise ValueError("#ERROR_RENDER: Unknown render mode!")

        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont("Arial", 100)

    def close(self):
        """
        Closes the pygame window.
        """
        pygame.quit()

    def get_rgb_array(self, board: np.ndarray) -> np.ndarray:
        """
        Returns the rgb image of the pygame window in (H, W, C) format.

        Args:
            board (np.ndarray): tictactoe board of shape (H, W)

        Returns:
            np.ndarray: np.array of shape (H, W, C)
        """
        self._draw_state(board)
        return np.transpose(np.array(pygame.surfarray.pixels3d(self._screen)), axes=(1, 0, 2))  # in (H, W, C) format

    def draw_step(self, history: list[np.ndarray]):
        """
        Draws a step from the tictactoe environment into a frame.

        Args:
            history (list[np.ndarray]): history of all previous states
        """
        for state in history[-2:]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self._screen.fill((255, 255, 255))
            self._draw_state(state)

            if self._mode == "human":
                pygame.display.flip()
            self._clock.tick(30)
            pygame.time.delay(1000)

    def _draw_state(self, board: np.ndarray):
        """
        Draws the given board into a frame.

        Args:
            board (np.ndarray): history of all previous states
        """
        # Draw the board
        self._draw_board((0, 0, 0), 10)

        # Get the middle position of each area in the screen
        for i in range(1, 2 * self.board_height + 1, 2):
            for j in range(1, 2 * self.board_width + 1, 2):
                if board[i // 2, j // 2] == self._your_symbol:
                    symbol, text_color = "X", self._your_color
                elif board[i // 2, j // 2] == self._enemy_symbol:
                    symbol, text_color = "O", self._enemy_color
                else:
                    continue
                # Draw each tile of the board
                self._draw_text(symbol, text_color, (
                    i * self.window_height // (self.board_height * 2),
                    j * self.window_width // (self.board_height * 2)))

    def _draw_board(
            self,
            board_color: tuple[int, int, int],  # in (R, G, B) format
            thickness: int,
    ):
        """
        Draws the TicTacToe Board as a frame.

        Args:
            board_color (tuple[int, int, int]): color of the lines on the screen in (R, G, B) format
            thickness (int): thickness of the lines
        """
        # Draw row lines
        for i in range(1, self.board_height):
            pygame.draw.line(self._screen, board_color, (0, i * self.window_height / self.board_height),
                             (self.window_width, i * self.window_height / self.board_height), thickness)

        # Draw column lines
        for i in range(1, self.board_width):
            pygame.draw.line(self._screen, board_color, (i * self.window_width / self.board_width, 0),
                             (i * self.window_width / self.board_width, self.window_height), thickness)

    def _draw_text(
            self,
            text: str,
            text_color: tuple[int, int, int],  # in (R, G, B) format
            pos: tuple[int, int],  # in (H, W) format
    ):
        """
        Draws a text as a frame.

        Args:
            text (str): included text
            text_color (tuple[int, int, int]): color of the text in (R, G, B) format
            pos (tuple[int, int]): middle position (as pixels) of the text in (H, W) format

        """
        img = self._font.render(text, True, text_color)
        center_pos = (pos[1] - img.get_width() // 2, pos[0] - img.get_height() // 2)
        self._screen.blit(img, center_pos)
