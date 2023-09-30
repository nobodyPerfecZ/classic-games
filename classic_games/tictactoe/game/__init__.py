import gymnasium as gym

# Register the environment
gym.register(
    id="TicTacToe-v0",  # Unique identifier for the environment
    entry_point="classic_games.tictactoe.game.env:TicTacToeEnv",  # Path to the environment class
)
