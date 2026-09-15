import numpy as np

A = [[1, 2], [3, 4]]

B = [[1, 2, 3], [5, 6, 7], [8, 9, 10], [11, 12, 13]]


def transpose_matrix(matrix: list[list[float]]):

    matrix_transpose = []
    for i in range(len(matrix[0])):
        row = []
        for j in range(len(matrix)):
            print(j, i)
            row.append(matrix[j][i])
        matrix_transpose.append(row)

    print(matrix_transpose)


transpose_matrix(B)
