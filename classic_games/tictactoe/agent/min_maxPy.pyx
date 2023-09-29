# distutils: language = c++
# distutils: sources = ./classic_games/tictactoe/agent/min_maxC.cpp ./classic_games/tictactoe/model/boardC.cpp ./classic_games/util/hasher.cpp

from libcpp.vector cimport vector
import numpy as np

cdef extern from "min_maxC.h":
    cdef cppclass MiniMaxC:        
        MiniMaxC(int, int, int, int)
        int get_best_action(vector[vector[int]] board)


cdef class MiniMax:
    cdef MiniMaxC* obj

    def __cinit__(self, int your_symbol = 1, int enemy_symbol = -1, int tiles_to_win = 3, int max_depth = np.iinfo(np.int32).max):
        assert max_depth >= 1, "#ERROR_MINMAXPY: max_depth should be higher or equal to 1!"
        self.obj = new MiniMaxC(your_symbol, enemy_symbol, tiles_to_win, max_depth)
    
    def __dealloc__(self):
        del self.obj

    def get_best_action(self, vector[vector[int]] board) -> int:
        """
        Returns the best action from the given state, according to the MiniMax algorithm.

        Args:
            board (ObsType): current state

        Returns:
            int: best action with the given state
        """
        return self.obj.get_best_action(board)