# distutils: language = c++
# distutils: sources = ./classic_games/tictactoe/model/boardC.cpp

from libcpp.vector cimport vector
import numpy as np

cdef extern from "boardC.h":
    cdef cppclass TicTacToeBoardC:
        TicTacToeBoardC(vector[vector[int]], int, int, int, bint)
        int row()
        int col()
        bint check_terminated()
        int check_winner()
        vector[vector[int]] get_current()
        vector[vector[vector[int]]] get_successors()
        vector[vector[vector[int]]] get_history()
        vector[int] get_actions()
        bint get_current_player()
        void set(int action)
        float get_reward()
        int get_your_corner_tiles()
        int get_enemy_corner_tiles()
        int get_your_middle_tiles()
        int get_enemy_middle_tiles()
        int get_immediate_winning_moves()
        int get_immediate_blocking_moves()

cdef class TicTacToeBoard:
    cdef TicTacToeBoardC* obj

    def __cinit__(self, vector[vector[int]] board, int tiles_to_win = 3, int your_symbol = 1, int enemy_symbol = -1, bint your_start = True):
        assert board.size() == board[0].size(), "#ERROR_BOARDPY: height and width should be the same!"
        assert board.size() >= 3, "#ERROR_BOARDPY: height and width should be at least 3!"
        assert tiles_to_win >= 3, "#ERROR_BOARDPY: number of tiles to win should be at least 3!"
        assert tiles_to_win <= board.size(), "#ERROR_BOARDPY: number of tiles cannot be longer than one dimension!"
        assert your_symbol != 0 and enemy_symbol != 0, "#ERROR_BOARDPY: symbol of you and enemy cannot be 0!"
        assert your_symbol != enemy_symbol, "#ERROR_BOARDPY: symbol of you and enemy cannot be the same!"
        
        self.obj = new TicTacToeBoardC(board, tiles_to_win, your_symbol, enemy_symbol, your_start)
    
    def __dealloc__(self):
        del self.obj

    @property
    def row(self) -> int:
        return self.obj.row()
    
    @property
    def col(self) -> int:
        return self.obj.col()
    
    def check_terminated(self) -> bool:
        """
        Returns True if the board is terminated state

        Returns:
            bool: True if the board is terminated state
        """
        return self.obj.check_terminated()
    
    def check_winner(self) -> int:
        """
        Returns the winner of the current board.

        Returns:
            int: 0 - no winner, your_symbol - your player wins, enemy_symbol - enemy player wins
        """
        return self.obj.check_winner()

    def get_current(self) -> np.ndarray:
        """
        Returns the current board state.

        Returns:
            np.ndarray: current board state
        """
        # Get the current board state
        cdef vector[vector[int]] current = self.obj.get_current()

        # Convert std::vector<std::vector<int>> into np.ndarray
        return np.array([[current[i][j] for j in range(len(current[i]))] for i in range(len(current))])

    def get_successors(self) -> list[np.ndarray]:
        """
        Returns the successor boards, if we take an action from the current board.

        Returns:
            list[np.ndarray]: list of successor boards
        """
        # Get the successor board states
        cdef vector[vector[vector[int]]] successors = self.obj.get_successors()

        # Convert std::vector<std::vector<std::vector<int>>> into list[np.ndarray]
        return [np.array([[successors[i][j][k] for k in range(len(successors[i][j]))] for j in range(len(successors[i]))]) for i in range(len(successors))]

    def get_history(self) -> list[np.ndarray]:
        """
        Returns the entire history of changes on the board.

        Returns:
            list[np.ndarray]: history of changes of the board
        """
        # Get the history
        cdef vector[vector[vector[int]]] history = self.obj.get_history()

        # Convert std::vector<std::vector<std::vector<int>>> into list[np.ndarray]
        return [np.array([[history[i][j][k] for k in range(len(history[i][j]))] for j in range(len(history[i]))]) for i in range(len(history))]
    
    def get_actions(self) -> list[int]:
        """
        Returns all possible actions of the board.

        Returns:
            list[int]: list of actions
        """
        # Get the list of actions
        cdef vector[int] actions = self.obj.get_actions()

        # Convert std::vector<int> into list[int]
        return [actions[i] for i in range(len(actions))]
    
    def get_current_player(self) -> bool:
        """
        Returns the current player as bool.

        Returns:
            bool: True if your player is the current player otherwise False
        """
        return self.obj.get_current_player()
    
    def set(self, action: int):
        """
        Sets a tile on the board according to the given action.

        Args:
            action (int): Encoding of the position (n*row + col), where the tile needs to be placed
        """
        self.obj.set(action)
    
    def get_reward(self) -> float:
        """
        Returns a reward of (...)
            - +1.0 if you won
            - -1.0 if enemy won
            - 0.0 if nobody won

        Returns:
            float: reward value of the current state
        """
        return self.obj.get_reward()

    ################################
    ####Feature-specific methods####
    ################################
    
    def get_your_corner_tiles(self) -> int:
        """
        Returns:
            int: number of your tiles, that are at the corner
        """
        return self.obj.get_your_corner_tiles()
    
    def get_enemy_corner_tiles(self) -> int:
        """
        Returns:
            int: number of enemy tiles, that are at the corner
        """
        return self.obj.get_enemy_corner_tiles()

    def get_your_middle_tiles(self) -> int:
        """
        Returns:
            int: number of your tiles, that are in the middle
        """
        return self.obj.get_your_middle_tiles()
    
    def get_enemy_middle_tiles(self) -> int:
        """
        Returns:
            int: number of enemy tiles, that are in the middle
        """
        return self.obj.get_enemy_middle_tiles()
    
    def get_immediate_winning_moves(self) -> int:
        """
        Returns:
            int: number of tiles, where an immediate move (next turn) refers to a win for your player.
        """
        return self.obj.get_immediate_winning_moves()
    
    def get_immediate_blocking_moves(self) -> int:
        """
        Returns:
            int: number of tiles, where an immediate move (next turn) refers to a block for a win of the enemy player.
        """
        return self.obj.get_immediate_blocking_moves()
