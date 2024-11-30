from matrix_pow import matrix_pow

m = [[1.0, 2.0], [3.0, 4.0]]

assert matrix_pow(m, 0) == [[1.0, 0.0], [0.0, 1.0]]
print(matrix_pow(m, 0))

assert matrix_pow(m, 1) == m
print(matrix_pow(m, 1))

assert matrix_pow(m, 3) == [[37.0, 54.0], [81.0, 118.0]]
print(matrix_pow(m, 3))
