#ifndef TICTACTOEBOARD_H
#define TICTACTOEBOARD_H

#include <vector>
#include <tuple>

class TicTacToeBoard {
    private:
        std::vector<std::vector<int>> board;
        int tiles_to_win;
        int your_symbol;
        int enemy_symbol;
        bool current_player;
        int winner;
        std::vector<std::vector<std::vector<int>>> history;

        /**
         * @brief Checks if the board is full (no action are possible anymore).
         * 
         * @return true if the board is full, otherwise false 
         */
        bool is_terminated();

        /**
         * @brief Checks if the given player have n tiles on the row, column, diagonal or anti-diagonal for the given position.
         * 
         * @param pos position of the board (row, col)
         * @param your_symbol Should it be checked for your player (:= True) or for the enemy (:= False).
         * 
         * @return true, if we have n tiles in the row, column diagonal or anti diagonal
         */
        bool winning_move(std::tuple<int, int> pos, bool your_symbol);

    public:
        
        /**
         * @brief Construct a new Tic Tac Toe Board object
         * 
         * @param board matrix of the game state
         * @param tiles_to_win number of tiles to place in row, column, diagonal, anti-diagonal to win the game
         * @param your_symbol symbol of your player
         * @param enemy_symbol symbol of enemy player
         * @param your_start your player starts
         */
        TicTacToeBoard(
            std::vector<std::vector<int>> board, 
            int tiles_to_win, 
            int your_symbol, 
            int enemy_symbol, 
            bool your_start
        );

        /**
         * @return int number of rows of the board
         */
        int row();

        /**
         * @return int number of columns of the board
         */
        int col();

        /**
         * @brief Returns true if the board is terminated state
         * 
         * @return bool true if board is terminated, otherwise false
         */
        bool check_terminated();

        /**
         * @brief Returns the winner of the current board.
         * 
         * @return int:
         *      0 - no winner
         *      your_symbol - your player wins
         *      enemy_symbol - enemy player wins
         */
        int check_winner();

        /**
         * @brief Returns the current board state.
         * 
         * @return std::vector<std::vector<int>> current board state
         */
        std::vector<std::vector<int>> get_current();
        
        /**
         * @brief Returns the number of successor boards given the current board
         * 
         * @return int number of successor boards
         */
        int get_successors_length();

        /**
         * @brief Returns all successor boards, if we take a single action from the current board.
         * 
         * @return std::vector<std::vector<std::vector<int>>> list of successor boards
         */
        std::vector<std::vector<std::vector<int>>> get_successors();
        
        /**
         * @brief Returns the length of the entire history of changes on the board.
         * 
         * @return int length of the entire history of changes
         */
        int get_history_length();

        /**
         * @brief Returns the entire history of changes on the board.
         * 
         * @return std::vector<std::vector<std::vector<int>>> history of changes of the board
         */
        std::vector<std::vector<std::vector<int>>> get_history();

        /**
         * @brief Returns the length of the output get_actions().
         * 
         * @return int length of output get_actions()
         */
        int get_actions_length();
        
        /**
         * @brief Returns all possible actions of the board.
         * 
         * @return std::vector<int> list of actions
         */
        std::vector<int> get_actions();
        
        /**
         * @brief Returns the current player as bool.
         * 
         * @return bool true if your player is the current player, otherwise false
         */
        bool get_current_player();
        
        /**
         * @brief Sets a tile on the board according to the given action
         * 
         * @param action Encoding of the position (n*row + col), where the tile needs to be placed
         */
        void set(int action);

        /**
         * @brief Returns a reward of (...)
         *      - +1.0 if your player won
         *      - -1.0 if enemy player won
         *      - 0.0 if nobody won (draw)
         * 
         * @return float reward value of the current state
         */
        float get_reward();

        //################################
        //###Feature-specific methods#####
        //################################

        /**
         * @return int number of tiles, where an immediate move (next turn) refers to a win for your player.
         */
        int get_immediate_winning_moves();

        /**
         * @return int number of tiles, where an immediate move (next turn) refers to a block for a win of the enemy player.
         */
        int get_immediate_blocking_moves();
};

#endif