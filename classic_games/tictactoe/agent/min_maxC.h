#ifndef MINMAX_H
#define MINMAX_H

#include "../../util/hasher.h"
#include <vector>
#include <tuple>
#include <unordered_map>
#include <limits>

class MiniMaxC {
    private:
        std::unordered_map<std::vector<std::vector<int>>, std::tuple<float, int>, decltype(&Hasher::matrix_hash)> cache;
        bool your_start = true;
        int depth = 0;
        float alpha = -std::numeric_limits<float>::infinity();
        float beta = std::numeric_limits<float>::infinity();
        int your_symbol;
        int enemy_symbol;
        int tiles_to_win;
        int max_depth = std::numeric_limits<int>::infinity();

        /**
         * @brief Resets the parameters of the minimax-search
         */
        void reset();

        /**
         * @brief The upper part from the Minimax algorithm, where we return the (reward, action) 
         * pair of a given state. If the state is non-terminated then go deeper in the tree.
         * 
         * @param board current state
         * @return std::tuple<float, int> (reward, action) pair of the current state
         */
        std::tuple<float, int> minimax(std::vector<std::vector<int>> board);

        /**
         * @brief The max-part of the Minimax algorithm. It returns 
         * the (reward, action) pair of a given state, so that 
         * we maximize our reward.
         * 
         * @param board current state
         * @return std::tuple<float, int> (reward, action) pair which maximizes our reward from the given state
         */
        std::tuple<float, int> max(std::vector<std::vector<int>> board);

        /**
         * @brief The min-part of the Minimax algorithm. It returns 
         * the (reward, action) pair of a given state, so that 
         * we minimize our reward.
         * 
         * @param board current state
         * @return std::tuple<float, int> (reward, action) pair which minimize our reward from the given state
         */
        std::tuple<float, int> min(std::vector<std::vector<int>> board);

    public:
        /**
         * @brief Construct a new MiniMaxC Object
         *
         * @param your_symbol symbol of your player
         * @param enemy_symbol symbol of enemy player
         * @param tiles_to_win number of tiles to place in row, column, diagonal, anti-diagonal to win the game
         * @param max_depth maximal depth for the minimax algorithm
         */
        MiniMaxC(int your_symbol, int enemy_symbol, int tiles_to_win, int max_depth) {
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

        /**
         * @brief Returns the best action from the given state, according to the MiniMax algorithm.
         * 
         * @param board current state
         * @return int best action with the given state
         */
        int get_best_action(std::vector<std::vector<int>> board);
};
#endif