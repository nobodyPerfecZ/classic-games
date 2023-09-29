#include "min_maxC.h"
#include "../model/boardC.h"
#include <iostream>

void MiniMaxC::reset() {
    this->your_start = true;
    this->depth = 0;
    this->alpha = -std::numeric_limits<float>::infinity();
    this->beta = std::numeric_limits<float>::infinity();
}

std::tuple<float, int> MiniMaxC::minimax(std::vector<std::vector<int>> board) {
    TicTacToeBoardC state = TicTacToeBoardC(
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

std::tuple<float, int> MiniMaxC::max(std::vector<std::vector<int>> board) {
    TicTacToeBoardC state = TicTacToeBoardC(
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


std::tuple<float, int> MiniMaxC::min(std::vector<std::vector<int>> board) {
    TicTacToeBoardC state = TicTacToeBoardC(
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

int MiniMaxC::get_best_action(std::vector<std::vector<int>> board) {
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
