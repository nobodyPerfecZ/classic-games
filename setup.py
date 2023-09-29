from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import argparse
import sys

# Build the argument parser for defining the used c++ version
argparser = argparse.ArgumentParser(description="Custom argument parser")
argparser.add_argument("--std", type=str, help="defines the used c++ version for the compiler", default="c++17", required=True)
args, unknown = argparser.parse_known_args()
sys.argv = [sys.argv[0]] + unknown

# Retrieve the c++ version
std = args.std

extensions = [
    Extension("classic_games.tictactoe.model.board", sources=["classic_games/tictactoe/model/boardPy.pyx", "classic_games/tictactoe/model/boardC.cpp"], extra_compile_args=[f"/std:{std}"]),
    Extension("classic_games.tictactoe.agent.min_max", sources=["classic_games/tictactoe/agent/min_maxPy.pyx", "classic_games/tictactoe/agent/min_maxC.cpp", "classic_games/tictactoe/model/boardC.cpp", "classic_games/util/hasher.cpp"], extra_compile_args=["/std:{std}"]),
]

# Load the requirements from requirements.txt
with open('requirements.txt') as f:
    req = f.read().splitlines()

setup(
    name="classic_games",
    version="0.1",
    author=["Dennis J.", "Patrick B."],
    python_requires=">=3.10",
    packages=find_packages(
        exclude=[
            "classic_games.chess",
            "classic_games.chess.*",
            "classic_games.connectfour",
            "classic_games.connectfour.*",
            "classic_games.snake",
            "classic_games.snake.*",
            "classic_games.sudoku",
            "classic_games.sudoku.*",
            "tests",
            "tests.*",
        ]),
    include_package_data=True,
    install_requires=req,
    ext_modules=cythonize(extensions, language_level="3"),
)
