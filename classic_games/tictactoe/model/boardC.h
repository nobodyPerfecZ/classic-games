#ifndef TICTACTOEBOARD_H
#define TICTACTOEBOARD_H

#include <vector>
#include <tuple>

class TicTacToeBoardC {
    private:
        /* */
        std::vector<std::vector<int>> board;
        /* number of places that one player needs to win the game */
        int tiles_to_win;
        /* symbol of your player on the board */
        int your_symbol;
        /* symbol of enemy player on the board */
        int enemy_symbol;
        /* which player makes the next turn */
        bool current_player;
        /* current winner of the game */
        int winner;
        /* list of boards which moves are done from beginning */
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
         * @brief Construct a new TicTacToeBoardC object
         * 
         * @param board matrix of the game state
         * @param tiles_to_win number of tiles to place in row, column, diagonal, anti-diagonal to win the game
         * @param your_symbol symbol of your player
         * @param enemy_symbol symbol of enemy player
         * @param your_start your player starts
         */
        TicTacToeBoardC(
            std::vector<std::vector<int>> board, 
            int tiles_to_win, 
            int your_symbol, 
            int enemy_symbol, 
            bool your_start
        ) {
            this->board = board;
            this->tiles_to_win = tiles_to_win;
            this->your_symbol = your_symbol;
            this->enemy_symbol = enemy_symbol;
            this->current_player = your_start;
            this->winner = 0;
            this->history.push_back(this->board);
        };

        /**
         * @brief Destructor of the TicTacToeBoardC
         */
        ~TicTacToeBoardC() {};

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
         * @brief Returns all successor boards, if we take a single action from the current board.
         * 
         * @return std::vector<std::vector<std::vector<int>>> list of successor boards
         */
        std::vector<std::vector<std::vector<int>>> get_successors();

        /**
         * @brief Returns the entire history of changes on the board.
         * 
         * @return std::vector<std::vector<std::vector<int>>> history of changes of the board
         */
        std::vector<std::vector<std::vector<int>>> get_history();
        
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
        //####Feature-specific methods####
        //################################
        
        /**
         * @return int number of your tiles, that are at the corner
         */
        int get_your_corner_tiles();

        /**
         * @return int number of enemy tiles, that are at the corner
         */
        int get_enemy_corner_tiles();

        /**
         * @return int number of your tiles, that are in the middle
         */
        int get_your_middle_tiles();

        /**
         * @return int number of enemy tiles, that are in the middle
         */
        int get_enemy_middle_tiles();

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