#ifndef CONVERTER_H
#define CONVERTER_H
#include <vector>

class Converter {
    public:
        /**
         * @brief Convert int* object into std::vector<int>
         * 
         * @param arr container for multiple elements
         * @param col number of columns of the given array
         * @return std::vector<int> array as vector
         */
        static std::vector<int> to_c_plus_vector(int* arr, int col);

        /**
         * @brief Convert int* object into std::vector<std::vector<int>>
         * 
         * @param matrix container for multiple arrays as elements
         * @param row number of rows of the given matrix
         * @param col number of columns of the given matrix
         * @return std::vector<std::vector<int>> matrix as vector of vector
         */
        static std::vector<std::vector<int>> to_c_plus_matrix(int* matrix, int row, int col);

        /**
         * @brief Convert std::vector<int> object into int*
         * 
         * @param arr container for multiple elements
         * @return int* array
         */
        static int* to_c_vector(std::vector<int> arr);

        /**
         * @brief Convert std::vector<std::vector<int>> into int* (row-wise).
         * E.g.:
         * matrix := 
         * [1, 2, 3]
         * [4, 5, 6]
         * [7, 8, 9]
         * 
         * to_c_matrix(matrix) := [1, 2, 3, 4, 5, 6, 7, 8, 9]
         * 
         * @param matrix container for multiple arrays as elements
         * @return int* matrix
         */
        static int* to_c_matrix(std::vector<std::vector<int>> matrix);

        /**
         * @brief Convert std::vector<std::vector<int>> into int*
         * 
         * @param matrices container for multiple matricies as elements
         * @return int* matricies
         */
        static int* to_c_list_matrix(std::vector<std::vector<std::vector<int>>> matrices);
};
#endif