#include "converter.h"
#include <cstdlib>

std::vector<int> Converter::to_c_plus_vector(int* arr, int col) {
    std::vector<int> result(col, 0);
    for (size_t i = 0; i < col; i++) {
        result[i] = arr[i];
    } 
    return result;
}

std::vector<std::vector<int>> Converter::to_c_plus_matrix(int* matrix, int row, int col) {
    std::vector<std::vector<int>> result(row, std::vector<int>(col, 0));
    for (size_t i = 0; i < row; i++) {
        for(size_t j = 0; j < col; ++j) {
            int index = i * col + j;
            result[i][j] = matrix[index];
        }
    }
    return result;
}

int* Converter::to_c_vector(std::vector<int> arr) {
    int* result = new int[arr.size()];
    for (size_t i = 0; i < arr.size(); i++) {
        result[i] = arr[i];
    }
    return result;
}

int* Converter::to_c_matrix(std::vector<std::vector<int>> matrix) {
    int first_dimension = 0;
    int second_dimension = 0;
    if (!matrix.empty() && !matrix[0].empty()) {
        // Case: Both dimensions are given
        first_dimension = matrix.size();
        second_dimension = matrix[0].size();
    }
    int* result = new int[first_dimension * second_dimension];
    int index = 0;
    for (size_t i = 0; i < first_dimension; i++) {
        for (size_t j = 0; j < second_dimension; j++) {
            result[index++] = matrix[i][j];
        }
    }
    return result;
}

int* Converter::to_c_list_matrix(std::vector<std::vector<std::vector<int>>> matrices) {
    int first_dimension = 0;
    int second_dimension = 0;
    int third_dimension = 0;
    if (!matrices.empty() && !matrices[0].empty() && !matrices[0][0].empty()) {
        // Case: At least one matrix is given
        first_dimension = matrices.size();
        second_dimension = matrices[0].size();
        third_dimension = matrices[0][0].size();
    }
    int* result = new int[first_dimension * second_dimension * third_dimension];
    int index = 0;
    for (size_t i = 0; i < first_dimension; i++) {
        for (size_t j = 0; j < second_dimension; j++) {
            for (size_t k = 0; k < third_dimension; k++) {
                result[index++] = matrices[i][j][k];
            }
        }
    }
    return result;
}