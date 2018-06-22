import numpy as np


class CompareMatrix(object):

    def __init__(self, size):
        self.__n = size
        # noinspection PyUnresolvedReferences
        self.__matrix = np.zeros(shape=(self.__n, self.__n))
        for i in range(self.__n):
            self.__matrix[i, i] = 1
        self.__categories = [None] * self.__n
        self.__perron_frobenius_eigenvalue = 0
        # noinspection PyUnresolvedReferences
        self.__perron_frobenius_eigenvector = np.zeros(shape=self.__n)

    def set_matrix_element(self, row_num, column_num, value):
        if row_num == column_num:
            self.__matrix[row_num - 1, column_num - 1] = 1
        else:
            self.__matrix[row_num - 1, column_num - 1] = value
            self.__matrix[column_num - 1, row_num - 1] = 1 / value

    def get_matrix_element(self, row_num, column_num):
        return self.__matrix[row_num - 1, column_num - 1]

    def set_matrix(self, array):
        for i in range(self.__n):
            for j in range(self.__n):
                self.set_matrix_element(i, j, array[i - 1, j - 1])

    def get_matrix(self):
        return self.__matrix

    def set_category(self, num, value):
        self.__categories[num - 1] = value

    def get_category(self, num):
        return self.__categories[num - 1]

    def set_categories(self, array):
        for i in range(self.__n):
            self.set_category(i, array[i - 1])

    def get_categories(self):
        return self.__categories

    def get_size(self):
        return self.__n

    def calculate(self):
        v, w = np.linalg.eig(self.__matrix)
        v = abs(v)
        w = abs(w)
        perron_position = np.argmax(v)
        self.__perron_frobenius_eigenvalue = v[perron_position]
        self.__perron_frobenius_eigenvector = w[:, perron_position]

    def get_perron_frobenius_eigenvalue(self):
        return self.__perron_frobenius_eigenvalue

    def perron_frobenius_eigenvector(self):
        return self.__perron_frobenius_eigenvector

    def get_weights(self):
        summa = sum(self.__perron_frobenius_eigenvector)
        return self.__perron_frobenius_eigenvector / summa

    def get_consistency_index(self):
        return (self.__perron_frobenius_eigenvalue - self.__n) / (self.__n - 1)

    def get_consistency_ratio(self):
        n_to_ri = {
            1: 0,
            2: 0,
            3: 0.52,
            4: 0.89,
            5: 1.11,
            6: 1.25,
            7: 1.35,
            8: 1.40,
            9: 1.45,
            10: 1.49,
            11: 1.51,
            12: 1.54,
            13: 1.56,
            14: 1.57,
            15: 1.58
        }
        if self.__n <= 15:
            result = self.get_consistency_index() / n_to_ri[self.__n]
        else:  # unable to define C.R.
            result = None
        return result

    def get_unsorted_result(self):
        weights = self.get_weights()
        result = []
        for i in range(len(self.__categories)):
            result.append([i + 1, self.__categories[i], weights[i]])
        return result

    def get_sorted_result(self):
        result = self.get_unsorted_result()
        result.sort(key=lambda lst: lst[2], reverse=True)
        return result

    def to_string(self):
        round_matrix = self.get_matrix()
        for i in range(self.__n):
            for j in range(self.__n):
                round_matrix[i, j] = round(round_matrix[i, j], 3)
        round_result = self.get_sorted_result()
        for i in range(self.__n):
            round_result[i][2] = round(round_result[i][2], 3)
        return ('Categories = ' + '\n' + str(self.get_categories()) + '\n' +
                'Matrix = ' + '\n' + str(round_matrix) + '\n' +
                'Perron-Frobenius eigenvalue = ' + str(round(self.get_perron_frobenius_eigenvalue(), 3)) + '\n' +
                'Perron-Frobenius eigenvector = ' + '\n' +
                str([round(v, 3) for v in self.perron_frobenius_eigenvector()]) + '\n' +
                'Weights = ' + '\n' + str([round(v, 3) for v in self.get_weights()]) + '\n' +
                'Consistency index = ' + str(round(self.get_consistency_index(), 3)) + '\n' +
                'Consistency ratio = ' + str(round(self.get_consistency_ratio(), 3)) + '\n' +
                'Sorted result = ' + '\n' + str(round_result))

