#include "min_max.h"
#include "../model/board.h"
#include "../../util/converter.h"
#include <iostream>

void MiniMax::reset() {
    this->your_start = true;
    this->depth = 0;
    this->alpha = -std::numeric_limits<float>::infinity();
    this->beta = std::numeric_limits<float>::infinity();
}

std::tuple<float, int> MiniMax::minimax(std::vector<std::vector<int>> board) {
    TicTacToeBoard state = TicTacToeBoard(
        board, 
        this->tiles_to_win, 
        this->your_symbol, 
        this->enemy_symbol, 
        this->your_start
    );
    if (state.check_terminated()) {
        // Case: Terminated state reached
        // Return the reward of the current state
        float reward = state.get_reward() * (2 * (state.row() * state.col()) - this->depth);
        return std::make_tuple(reward, -1);
    } else if (this->depth == this->max_depth) {
        // Case: Max depth is reached
        // Use features as rewards
        float reward = 0.0;
        if (this->your_start) {
            reward = - this->depth;
        } else {
            reward = + this->depth;
        }
        /*
        TODO: Fix the features
        if (this->your_start) {
            reward = state.get_immediate_winning_moves() - state.get_immediate_blocking_moves() - this->depth;
        } else {
            reward = state.get_immediate_winning_moves() - state.get_immediate_blocking_moves() + this->depth;
        }
        */
        return std::make_tuple(reward, -1);
    } else if (this->your_start) {
        // Case: Max player makes a turn
        return this->max(board);
    } else {
        // Case: Min player makes a turn
        return this->min(board);
    }
}

std::tuple<float, int> MiniMax::max(std::vector<std::vector<int>> board) {
    TicTacToeBoard state = TicTacToeBoard(
        board, 
        this->tiles_to_win, 
        this->your_symbol, 
        this->enemy_symbol, 
        true
    );
    std::tuple<float, int> best_v = std::make_tuple(-std::numeric_limits<float>::infinity(), -1);
    int cur_depth = this->depth;
    float cur_alpha = this->alpha;

    std::vector<std::vector<std::vector<int>>> successors = state.get_successors();
    std::vector<int> actions = state.get_actions();
    for (size_t i = 0; i < successors.size(); i++) {
        // Get the successor state with the given action
        std::vector<std::vector<int>> successor = successors[i];
        int action = actions[i];

        // Update the parameters
        this->depth = cur_depth + 1;
        this->your_start = false;

        std::tuple<float, int> v = this->minimax(successor);
        if (std::get<0>(v) > std::get<0>(best_v)) {
            best_v = std::make_tuple(std::get<0>(v), action);
        }
        if (std::get<0>(best_v) >= this->beta) {
            this->alpha = cur_alpha;
            return best_v;
        }
        this->alpha = std::max(this->alpha, std::get<0>(best_v));
    }
    this->alpha = cur_alpha;
    return best_v;
}


std::tuple<float, int> MiniMax::min(std::vector<std::vector<int>> board) {
    TicTacToeBoard state = TicTacToeBoard(
        board, 
        this->tiles_to_win,
        this->your_symbol, 
        this->enemy_symbol, 
        false
    );
    std::tuple<float, int> best_v = std::make_tuple(std::numeric_limits<float>::infinity(), -1);
    int cur_depth = this->depth;
    float cur_beta = this->beta;

    std::vector<std::vector<std::vector<int>>> successors = state.get_successors();
    std::vector<int> actions = state.get_actions();
    for (size_t i = 0; i < successors.size(); i++) {
        // Get the successor state with the given action
        std::vector<std::vector<int>> successor = successors[i];
        int action = actions[i];

        // Update the parameters
        this->depth = cur_depth + 1;
        this->your_start = true;

        std::tuple<float, int> v = this->minimax(successor);
        if (std::get<0>(v) < std::get<0>(best_v)) {
            best_v = std::make_tuple(std::get<0>(v), action);
        }
        if (std::get<0>(best_v) <= this->alpha) {
            this->beta = cur_beta;
            return best_v;
        }
        this->beta = std::min(this->beta, std::get<0>(best_v));
    }
    this->beta = cur_beta;
    return best_v;
}

MiniMax::MiniMax(int your_symbol, int enemy_symbol, int tiles_to_win, int max_depth) {
    this->cache = std::unordered_map<std::vector<std::vector<int>>, std::tuple<float, int>, decltype(&Hasher::matrix_hash)>(10, Hasher::matrix_hash);
    this->your_start = true;
    this->depth = 0;
    this->alpha = -std::numeric_limits<float>::infinity();
    this->beta = std::numeric_limits<float>::infinity();
    this->your_symbol = your_symbol;
    this->enemy_symbol = enemy_symbol;
    this->tiles_to_win = tiles_to_win;
    this->max_depth = max_depth;
}

int MiniMax::get_best_action(std::vector<std::vector<int>> board) {
    if (this->cache.count(board) > 0) {
        // Case: Board state was already evaluated
        std::tuple<float, int> result = this->cache[board];
        float reward = std::get<0>(result);
        int action = std::get<1>(result);
        return action;
    }

    // Reset the parameters
    this->reset();

    // Perform the minimax algorithm (with alpha-beta pruning)
    std::tuple<float, int> result = this->minimax(board);
    
    // Safe the results in the cache
    this->cache[board] = result;

    // Return the action
    float reward = std::get<0>(result);
    int action = std::get<1>(result);
    return action;
} 

// ctypes wrapper
extern "C" {
    /**
     * @brief Wrapper Function for MiniMax()
     */
    MiniMax* create_MiniMax(int your_symbol, int enemy_symbol, int tiles_to_win, int max_depth) {
        return new MiniMax(your_symbol, enemy_symbol, tiles_to_win, max_depth);
    }

    /**
     * @brief Wrapper Function for get_best_action()
     */
    int get_best_action(MiniMax* obj, int* board, int row, int col) {
        return obj->get_best_action(Converter::to_c_plus_matrix(board, row, col));
    }
}
