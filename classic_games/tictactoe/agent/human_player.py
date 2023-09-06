from typing import Optional
from gymnasium.core import ObsType

from classic_games.tictactoe.agent.abstract_player import Player
from classic_games.tictactoe.model.board import TicTacToeBoard


class HumanPlayer(Player):

    def __init__(
            self,
            your_symbol: int,
            enemy_symbol: int,
            tiles_to_win: int,
            player_name: str = "Human Player",
            seed: Optional[int] = None
    ):
        super().__init__(your_symbol, enemy_symbol, tiles_to_win, player_name, seed)

    def start(self, board: ObsType) -> int:
        # Update turns
        self._turn += 1

        state = TicTacToeBoard(board)
        actions = state.get_actions()

        if not actions:
            # Case: There is no valid actions to take anymore
            return None

        # Wait for human to type a number between 0-8
        while True:
            user_input = input(f"Please enter a number from {actions}: ")
            try:
                action = int(user_input)
                if action in actions:
                    print("You entered a valid number: ", action)
                    break
                else:
                    print("You entered an invalid number: ", action)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        return action

    def act(self, board: ObsType) -> int:
        # TODO: Implement here
        if self._turn == 0:
            return self.start(board)
        else:
            # Update turns
            self._turn += 1

            state = TicTacToeBoard(board)
            actions = state.get_actions()

            if not actions:
                # Case: There is no valid actions to take anymore
                return None

            # Wait for human to type a number between 0-8
            while True:
                user_input = input(f"Please enter a number from {actions}: ")
                try:
                    action = int(user_input)
                    if action in actions:
                        print("You entered a valid number: ", action)
                        break
                    else:
                        print("You entered an invalid number: ", action)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            return action

    def end(self, board: ObsType) -> int:
        pass
