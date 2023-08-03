import numpy as np
import pygame


class TicTacToeRender:

    def __init__(
            self,
            window_shape: tuple[int, int],  # in (H, W) format
            board_shape: tuple[int, int],  # in (H, W) format
            your_symbol: int,
            enemy_symbol: int,
            your_color: tuple[int, int, int] = (0, 128, 0),  # in (R, G, B) format
            enemy_color: tuple[int, int, int] = (255, 0, 0),  # in (R, G, B) format
            caption: str = "TicTacToe-v0",
    ):
        self._window_shape = window_shape
        self._board_shape = board_shape
        self._your_symbol = your_symbol
        self._enemy_symbol = enemy_symbol
        self._your_color = your_color
        self._enemy_color = enemy_color
        self._caption = caption

        self._screen = None
        self._clock = None
        self._font = None

    def init(self):
        """
        TODO: Add Documentation
        """
        # Start the pygame window
        pygame.init()
        self._screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self._caption)
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont("Arial", 100)

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

    def draw_game(self, history: list[np.ndarray]):
        """
        # TODO: Add Documentation
        """
        for state in history:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self._screen.fill((255, 255, 255))
            self._draw_state(state)

            pygame.display.flip()
            self._clock.tick(30)
            pygame.time.delay(1000)

    def _draw_state(self, board: np.ndarray):
        """
        # TODO: Add Documentation
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
        # TODO: Add Documentation
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
        # TODO: Add Documentation
        """
        img = self._font.render(text, True, text_color)
        center_pos = (pos[1] - img.get_width() // 2, pos[0] - img.get_height() // 2)
        self._screen.blit(img, center_pos)


if __name__ == "__main__":
    render = TicTacToeRender(
        window_shape=(400, 600),
        board_shape=(3, 3),
        your_symbol=1,
        enemy_symbol=-1,
    )

    states = [
        np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]),
        np.array([[1, -1, 0], [0, 0, 0], [0, 0, 0]]),
        np.array([[1, -1, 1], [0, 0, 0], [0, 0, 0]]),
        np.array([[1, -1, 1], [-1, 0, 0], [0, 0, 0]]),
        np.array([[1, -1, 1], [-1, 1, 0], [0, 0, 0]]),
        np.array([[1, -1, 1], [-1, 1, -1], [0, 0, 0]]),
        np.array([[1, -1, 1], [-1, 1, -1], [1, 0, 0]]),
        np.array([[1, -1, 1], [-1, 1, -1], [1, -1, 0]]),
        np.array([[1, -1, 1], [-1, 1, -1], [1, -1, 1]]),
    ]
    render.init()
    render.draw_game(states)
