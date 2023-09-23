from setuptools import setup, find_packages

setup(
    name="classic_games",
    version="0.0.1",
    packages=find_packages(
        exclude=[
            "classic_games.connectfour",
            "classic_games.connectfour.*",
            "classic_games.sudoku",
            "classic_games.sudoku.*",
            "classic_games.tests",
            "classic_games.tests.*"
        ]),
    author="Dennis J.",
    install_requires=[
        "gymnasium",
        "numpy",
    ],
)

# setup(
#     name="MiniMax",
#     ext_modules=cythonize("./classic_games/tictactoe/agent/min_max_player.pyx"),
# )
