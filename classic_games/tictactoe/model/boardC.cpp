#include "boardC.h"
#include <iostream>
#include <cstdlib>

bool TicTacToeBoardC::is_terminated() {
    for (const std::vector<int>& row: this->board) {
        for (int elem : row) {
            if (elem == 0) {
                return false;
            }
        }
    }
    return true;
}

bool TicTacToeBoardC::winning_move(std::tuple<int, int> pos, bool your_symbol) {
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

int TicTacToeBoardC::row() {
    return static_cast<int>(this->board.size());
}

int TicTacToeBoardC::col() {
    return static_cast<int>(this->board[0].size());
}

bool TicTacToeBoardC::check_terminated() {
    // Check if the game is over (win or draw)
    this->winner = this->check_winner();

    // Check if the game is finished (either someone won or all tiles are placed)
    if (this->winner || this->is_terminated()) {
        return true;
    }
    return false;

}

int TicTacToeBoardC::check_winner() {
    for (int i = 0; i < this->row(); i++) {
        for (int j = 0; j < this->col(); j++) {
            if (this->board[i][j] == 0) {
                // Case: No tile placed
                continue;
            } else if (this->winning_move(std::make_tuple(i, j), true)) {
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

std::vector<std::vector<int>> TicTacToeBoardC::get_current() {
    return this->board;
}

std::vector<std::vector<std::vector<int>>> TicTacToeBoardC::get_successors() {
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

std::vector<std::vector<std::vector<int>>> TicTacToeBoardC::get_history() {
    return this->history;
}

std::vector<int> TicTacToeBoardC::get_actions() {
    // Flatten the vector
    std::vector<int> board_vec;
    for (int i = 0; i < static_cast<int>(this->board.size()); i++) {
        for (int j = 0; j < static_cast<int>(this->board[i].size()); j++) {
            board_vec.push_back(this->board[i][j]);
        }
    }
    // Get all possible actions
    std::vector<int> actions;
    for (int i = 0; i < static_cast<int>(board_vec.size()); i++) {
        if (board_vec[i] == 0) {
            actions.push_back(i);
        }
    }
    return actions;
}

bool TicTacToeBoardC::get_current_player() {
    return this->current_player;
}

void TicTacToeBoardC::set(int action) {
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

float TicTacToeBoardC::get_reward() {
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

int TicTacToeBoardC::get_your_corner_tiles() {
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

int TicTacToeBoardC::get_enemy_corner_tiles() {
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

int TicTacToeBoardC::get_your_middle_tiles() {
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

int TicTacToeBoardC::get_enemy_middle_tiles() {
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

int TicTacToeBoardC::get_immediate_winning_moves() {
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

int TicTacToeBoardC::get_immediate_blocking_moves() {
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
