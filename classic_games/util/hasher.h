#ifndef HASHER_H
#define HASHER_H
#include <vector>

class Hasher {
    public:
        /**
         * @brief Calculates the hash of a matrix.
         * 
         * @param matrix container for multiple arrays as elements
         * @return std::size_t hash of the matrix
         */
        static std::size_t matrix_hash(const std::vector<std::vector<int>>& matrix);
};
#endif