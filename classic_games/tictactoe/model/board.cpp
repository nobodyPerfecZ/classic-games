#include "board.h"
#include "../../util/converter.h"
#include <iostream>
#include <cstdlib>

bool TicTacToeBoard::is_terminated() {
    for (const std::vector<int>& row: this->board) {
        for (int elem : row) {
            if (elem == 0) {
                return false;
            }
        }
    }
    return true;
}

bool TicTacToeBoard::winning_move(std::tuple<int, int> pos, bool your_symbol) {
    // Check for right inputs
    if (std::tuple_size<decltype(pos)>::value != 2) {
        std::cerr << "#ERROR_TICTACTOEBOARD: pos should be a tuple in form (row, col)!";
        std::abort();
    } else if (std::get<0>(pos) < 0 || this->row() <= std::get<0>(pos)) {
        // Case: row position is out of bounds!
        std::cerr << "#ERROR_TICTACTOEBOARD: row is out of bounds!";
        std::abort();
    } else if (std::get<1>(pos) < 0 || this->col() <= std::get<1>(pos)) {
        std::cerr << "#ERROR_TICTACTOEBOARD: col is out of bounds!";
        std::abort();
    }

    int row = std::get<0>(pos);
    int col = std::get<1>(pos);
    int symbol = 0;
    if (your_symbol) {
        symbol = this->your_symbol;
    } else {
        symbol = this->enemy_symbol;
    }

    // Check for rows
    int count = 0;
    for (int c = 0; c < this->col(); c++) {
        int tile = this->board[row][c];
        if (tile == symbol) {
            count++;
        } else {
            count = 0;
        }
        if (count >= this->tiles_to_win) {
            return true;
        }
    }

    // Check for columns
    count = 0;
    for (int r = 0; r < this->row(); r++) {
        int tile = this->board[r][col];
        if (tile == symbol) {
            count++;
        } else {
            count = 0;
        }
        if (count >= this->tiles_to_win) {
            return true;
        }
    }

    // Check for diagonals
    count = 0;
    int r = row - std::min(row, col);
    int c = col - std::min(row, col);
    for (int i = 0; i < std::min(this->row() - r, this->col() - c); i++) {
        int tile = this->board[r + i][c + i];
        if (tile == symbol) {
            count++;
        } else {
            count = 0;
        }
        if (count >= this->tiles_to_win) {
            return true;
        }
    }

    // Check for anti-diagonals
    count = 0;
    r = row - std::min(row, this->col() - 1 - col);
    c = col - std::min(row, this->col() - 1 - col);
    for (int i = 0; i < std::abs(r - c) + 1; i++) {
        int tile = this->board[r + i][c - i];
        if (tile == symbol) {
            count++;
        } else {
            count = 0;
        }
        if (count >= this->tiles_to_win) {
            return true;
        }
    }
    return false;
}

TicTacToeBoard::TicTacToeBoard(
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

int TicTacToeBoard::row() {
    return this->board.size();
}

int TicTacToeBoard::col() {
    return this->board[0].size();
}

bool TicTacToeBoard::check_terminated() {
    // Check if the game is over (win or draw)
    this->winner = this->check_winner();

    // Check if the game is finished (either someone won or all tiles are placed)
    if (this->winner || this->is_terminated()) {
        return true;
    }
    return false;

}

int TicTacToeBoard::check_winner() {
    for (int i = 0; i < this->row(); i++) {
        for (int j = 0; j < this->col(); j++) {
            if (this->winning_move(std::make_tuple(i, j), true)) {
                // Case: Your player won
                return this->your_symbol;
            } else if (this->winning_move(std::make_tuple(i, j), false)) {
                // Case: Enemy player won
                return this->enemy_symbol;
            }
        }
    }
    return 0;
}

std::vector<std::vector<int>> TicTacToeBoard::get_current() {
    return this->board;
}

int TicTacToeBoard::get_successors_length() {
    return this->get_successors().size();
}

std::vector<std::vector<std::vector<int>>> TicTacToeBoard::get_successors() {
    std::vector<std::vector<std::vector<int>>> successors;
    std::vector<int> actions = this->get_actions();
    std::vector<std::vector<int>> current_board = this->board;
    for (int action : actions) {
        // Create the successor state
        this->set(action);

        // Append the successor state into the list of successors
        successors.push_back(this->board);

        // Reset the board
        this->current_player = !this->current_player;
        this->board = current_board;
        this->history.pop_back();
    }
    return successors;
}

int TicTacToeBoard::get_history_length() {
    return this->history.size();
}

std::vector<std::vector<std::vector<int>>> TicTacToeBoard::get_history() {
    return this->history;
}

int TicTacToeBoard::get_actions_length() {
    int count = 0;
    for(size_t i = 0; i < this->row(); i++) {
        for (size_t j = 0; j < this->col(); j++) {
            if (this->board[i][j] == 0) {
                count++;
            }
        }
    }
    return count;
}

std::vector<int> TicTacToeBoard::get_actions() {
    // Flatten the vector
    std::vector<int> board_vec;
    for (int i = 0; i < this->board.size(); i++) {
        for (int j = 0; j < this->board[i].size(); j++) {
            board_vec.push_back(this->board[i][j]);
        }
    }
    // Get all possible actions
    std::vector<int> actions;
    for (int i = 0; i < board_vec.size(); i++) {
        if (board_vec[i] == 0) {
            actions.push_back(i);
        }
    }
    return actions;
}

bool TicTacToeBoard::get_current_player() {
    return this->current_player;
}

void TicTacToeBoard::set(int action) {
    int row = action / this->row();
    int col = action % this->col();

    if (this->board[row][col] == 0) {
        // Case: Position is empty
        if (this->current_player) {
            this->board[row][col] = this->your_symbol;
        } else {
            this->board[row][col] = this->enemy_symbol;
        }

        // Update the current player
        this->current_player = !this->current_player;

        // Update the history
        this->history.push_back(this->board);
    } else {
        // Case: Position is already taken
        std::cerr << "#ERROR_TICTACTOEBOARD: action is invalid!";
        std::abort();
    }
}

float TicTacToeBoard::get_reward() {
    if (this->winner == this->your_symbol) {
        // Case: Player1 won the game
        // Return a reward of 1.0
        return 1.0;
    } else if (this->winner == this->enemy_symbol) {
        // Case: Player2 won the game
        // Return a reward of -1.0
        return -1.0;
    } else if (this->winner == 0) {
        // Case: Nobody won the game
        // Return a reward of 0.0
        return 0.0;
    } else {
        std::cerr << "#ERROR_TICTACTOEBOARD: Unknown winner state!";
        std::abort();
    }
}

//################################
//####Feature-specific methods####
//################################

int TicTacToeBoard::get_your_corner_tiles() {
    int counter = 0;
    if (this->board[0][0] == this->your_symbol) {
        // Case: top left corner
        counter++;
    }
    if (this->board[0][this->col()-1] == this->your_symbol) {
        // Case: top right corner
        counter++;
    }
    if (this->board[this->row()-1][0] == this->your_symbol) {
        // Case: bottom left corner
        counter++;
    }
    if (this->board[this->row()-1][this->col()-1] == this->your_symbol) {
        // Case: bottom right corner
        counter++;
    }
    return counter;
}

int TicTacToeBoard::get_enemy_corner_tiles() {
    int counter = 0;
    if (this->board[0][0] == this->enemy_symbol) {
        // Case: top left corner
        counter++;
    }
    if (this->board[0][this->col()-1] == this->enemy_symbol) {
        // Case: top right corner
        counter++;
    }
    if (this->board[this->row()-1][0] == this->enemy_symbol) {
        // Case: bottom left corner
        counter++;
    }
    if (this->board[this->row()-1][this->col()-1] == this->enemy_symbol) {
        // Case: bottom right corner
        counter++;
    }
    return counter;
}

int TicTacToeBoard::get_your_middle_tiles() {
    int counter = 0;
    for (int i = 1; i < this->row()-1; i++) {
        for (int j = 1; j < this->col()-1; j++) {
            if (this->board[i][j] == this->your_symbol) {
                counter++;
            }
        }
    }
    return counter;
}

int TicTacToeBoard::get_enemy_middle_tiles() {
    int counter = 0;
    for (int i = 1; i < this->row()-1; i++) {
        for (int j = 1; j < this->col()-1; j++) {
            if (this->board[i][j] == this->enemy_symbol) {
                counter++;
            }
        }
    }
    return counter;
}

int TicTacToeBoard::get_immediate_winning_moves() {
    int winning_moves = 0;
    for (int i = 0; i < this->row(); i++) {
        for (int j = 0; j < this->col(); j++) {
            if (this->board[i][j] == 0) {
                // Case: Check if you would win if you place your symbol on this tile
                this->board[i][j] = this->your_symbol;
                if (this->winning_move(std::make_tuple(i, j), true)) {
                    // Case: Your player won
                    winning_moves++;
                }
                // Reset the move
                this->board[i][j] = 0;
            }
        }
    }
    return winning_moves;
}

int TicTacToeBoard::get_immediate_blocking_moves() {
    int blocking_moves = 0;
    for (int i = 0; i < this->row(); i++) {
        for (int j = 0; j < this->col(); j++) {
            if (this->board[i][j] == 0) {
                // Case: Check if you would win if you place your symbol on this tile
                this->board[i][j] = this->enemy_symbol;
                if (this->winning_move(std::make_tuple(i, j), false)) {
                    // Case: Your player won
                    blocking_moves++;
                }
                // Reset the move
                this->board[i][j] = 0;
            }
        }
    }
    return blocking_moves;
}

// ctypes wrapper
extern "C" {
    /**
     * @brief Wrapper Function to free allocated memory
     */
    void delete_TicTacToeBoard(TicTacToeBoard* obj) {
        delete obj;
    }

    /**
     * @brief Wrapper Function to free allocated memory
     */
    void delete_vector(int* arr) {
        delete arr;
    }

    /**
     * @brief Wrapper Function for TicTacToeBoard()
     */
    TicTacToeBoard* create_TicTacToeBoard(
        int* board, 
        int row, 
        int col,
        int tiles_to_win,
        int your_symbol,
        int enemy_symbol,
        bool your_start
    ) {
        return new TicTacToeBoard(Converter::to_c_plus_matrix(board, row, col), tiles_to_win, your_symbol, enemy_symbol, your_start);
    }

    /**
     * @brief Wrapper Function for row()
     */
    int row(TicTacToeBoard* obj) {
        return obj->row();
    }

    /**
     * @brief Wrapper Function for col()
     */
    int col(TicTacToeBoard* obj) {
        return obj->col();
    }

    /**
     * @brief Wrapper Function for check_terminated()
     */
    bool check_terminated(TicTacToeBoard* obj) {
        return obj->check_terminated();
    }

    /**
     * @brief Wrapper Function for check_winner()
     */
    int check_winner(TicTacToeBoard* obj) {
        return obj->check_winner();
    }

    /**
     * @brief Wrapper Function for get_current()
     */
    int* get_current(TicTacToeBoard* obj) {
        return Converter::to_c_matrix(obj->get_current());
    }

    /**
     * @brief Wrapper Function for get_successors_length()
     */
    int get_successors_length(TicTacToeBoard* obj) {
        return obj->get_successors_length();
    }

    /**
     * @brief Wrapper Function for get_successors()
     */
    int* get_successors(TicTacToeBoard* obj) {
        return Converter::to_c_list_matrix(obj->get_successors());
    }

    /**
     * @brief Wrapper Function for get_history_length()
     */
    int get_history_length(TicTacToeBoard* obj) {
        return obj->get_history_length();
    }

    /**
     * @brief Wrapper Function for get_history()
     */
    int* get_history(TicTacToeBoard* obj) {
        return Converter::to_c_list_matrix(obj->get_history());
    }

    /**
     * @brief Wrapper Function for get_actions_length()
     */
    int get_actions_length(TicTacToeBoard* obj) {
        return obj->get_actions_length();
    }

    /**
     * @brief Wrapper Function for get_actions()
     * 
     * @param obj 
     * @return std::vector<int> 
     */
    int* get_actions(TicTacToeBoard* obj) {
        return Converter::to_c_vector(obj->get_actions());
    }

    /**
     * @brief Wrapper Function for get_current_player()
     */
    bool get_current_player(TicTacToeBoard* obj) {
        return obj->get_current_player();
    }

    /**
     * @brief Wrapper Function for set(int action)
     */
    void set(TicTacToeBoard* obj, int action) {
        obj->set(action);
    }

    /**
     * @brief Wrapper Function for get_reward()
     */
    float get_reward(TicTacToeBoard* obj) {
        return obj->get_reward();
    }

    /**
     * @brief Wrapper Function for get_your_corner_tiles()
     */
    int get_your_corner_tiles(TicTacToeBoard* obj) {
        return obj->get_your_corner_tiles();
    }
    
    /**
     * @brief Wrapper Function for get_enemy_corner_tiles()
     */
    int get_enemy_corner_tiles(TicTacToeBoard* obj) {
        return obj->get_enemy_corner_tiles();
    }

    /**
     * @brief Wrapper Function for get_your_middle_tiles()
     */
    int get_your_middle_tiles(TicTacToeBoard* obj) {
        return obj->get_your_middle_tiles();
    }

    /**
     * @brief Wrapper Function for get_enemy_middle_tiles()
     */
    int get_enemy_middle_tiles(TicTacToeBoard* obj) {
        return obj->get_enemy_middle_tiles();
    }

    /**
     * @brief Wrapper Function for get_immediate_winning_moves()
     */
    int get_immediate_winning_moves(TicTacToeBoard* obj) {
        return obj->get_immediate_winning_moves();
    }

    /**
     * @brief Wrapper Function for get_immediate_blocking_moves()
     */
    int get_immediate_blocking_moves(TicTacToeBoard* obj) {
        return obj->get_immediate_blocking_moves();
    }
}