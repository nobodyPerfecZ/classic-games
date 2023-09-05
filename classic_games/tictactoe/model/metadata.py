from dataclasses import dataclass, asdict, field


@dataclass(frozen=True)
class Metadata:
    """
    Args:
        board_shape (tuple[int, int]):
            shape of the matrix.
            Defaults to (3, 3)
        tiles_to_win (int):
            number of tiles to place in row, column, diagonal, anti-diagonal to win the game.
            Defaults to 3.
        your_symbol (int):
            symbol of your player.
            Defaults to 1.
        enemy_symbol (int):
            symbol of enemy player.
            Defaults to -1
    """
    board_shape: tuple[int, int] = (3, 3)
    tiles_to_win: int = 3
    your_symbol: int = 1
    enemy_symbol: int = -1
    render_modes: list[str] = field(default_factory=lambda: ["human", "rgb_array"])
    render_fps: int = 30

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the dataclass.
        """
        return asdict(self)
