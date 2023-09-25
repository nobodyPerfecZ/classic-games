#include "hasher.h"
#include <functional>

std::size_t Hasher::matrix_hash(const std::vector<std::vector<int>>& matrix) {
    std::size_t seed = matrix.size();
    std::hash<int> int_hasher;
    for(int i = 0; i < matrix.size(); i++) {
        for(int j = 0; j < matrix[i].size(); j++) {
            int elem = matrix[i][j];
            elem = ((elem >> 16) ^ elem) * 0x45d9f3b;
            elem = ((elem >> 16) ^ elem) * 0x45d9f3b;
            elem = (elem >> 16) ^ elem;
            seed ^= int_hasher(elem) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        }
    }
  return seed;
}