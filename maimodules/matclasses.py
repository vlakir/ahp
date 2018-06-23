import numpy as np
import maimodules.utils as ut


class CompareMatrix(object):

    def __init__(self, size):
        self.__n = size
        # noinspection PyUnresolvedReferences
        self.__matrix = np.zeros(shape=(self.__n, self.__n))
        for i in range(self.__n):
            self.__matrix[i, i] = 1
        self.__categories = [None] * self.__n
        self.__main_eigenvalue = 0
        # noinspection PyUnresolvedReferences
        self.__main_eigenvector = np.zeros(shape=self.__n)

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
        self.__main_eigenvalue = v[perron_position]
        self.__main_eigenvector = w[:, perron_position]

    def get_main_eigenvalue(self):
        return self.__main_eigenvalue

    def main_eigenvector(self):
        return self.__main_eigenvector

    def get_weights(self):
        summa = sum(self.__main_eigenvector)

        if summa != 0:
            result = self.__main_eigenvector / summa
        else:
            result = self.__main_eigenvector * 0
        return result

    def get_consistency_index(self):
        return (self.__main_eigenvalue - self.__n) / (self.__n - 1)

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
        else:  # no empirical data to exactly define C.R.
            result = 1.59
        return result

    def get_unsorted_result(self):
        return ut.glue_result(self.__categories, self.get_weights(), False)

    def get_sorted_result(self):
        return ut.glue_result(self.__categories, self.get_weights(), True)

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
                'Main eigenvalue = ' + str(round(self.get_main_eigenvalue(), 3)) + '\n' +
                'Main eigenvector = ' + '\n' +
                str([round(v, 3) for v in self.main_eigenvector()]) + '\n' +
                'Weights = ' + '\n' + str([round(v, 3) for v in self.get_weights()]) + '\n' +
                'C.I. = ' + str(round(self.get_consistency_index(), 3)) + '\n' +
                'C.R. = ' + str(round(self.get_consistency_ratio(), 3)) + '\n' +
                'Sorted result = ' + '\n' + str(round_result))


class AhpContainer(object):
    def __init__(self, alternatives, factors):
        self.__factors = factors
        self.__alternatives = alternatives
        self.__factors_compare_matrix = CompareMatrix(len(factors))
        self.__factors_compare_matrix.set_categories(self.__factors)

        self.__alternatives_compare_matrixes = []
        for i in range(len(factors)):
            acm = CompareMatrix(len(alternatives))
            acm.set_categories(self.__alternatives)
            self.__alternatives_compare_matrixes.append(acm)

    def get_factors_count(self):
        return len(self.__factors)

    def get_alternatives_count(self):
        return len(self.__alternatives)

    def set_factors_compare_matrix_element(self, row_num, column_num, value):
        self.__factors_compare_matrix.set_matrix_element(row_num, column_num, value)

    def set_alternatives_compare_matrixes_element(self, matrix_num, row_num, column_num, value):
        self.__alternatives_compare_matrixes[matrix_num - 1].set_matrix_element(row_num, column_num, value)

    def set_factors_compare_matrix_elements(self, array):
        self.__factors_compare_matrix.set_matrix(array)

    def set_alternatives_compare_matrixes_elements(self, matrix_num, array):
        self.__alternatives_compare_matrixes[matrix_num - 1].set_matrix(array)

    def calculate(self):
        self.__factors_compare_matrix.calculate()
        for i in range(len(self.__factors)):
            self.__alternatives_compare_matrixes[i].calculate()

    def to_string(self):
        result = '=============================================================================' + '\n'
        result += '** Factors compare matrix **' + '\n'
        result += self.__factors_compare_matrix.to_string() + '\n\n'
        result += '=============================================================================' + '\n'
        result += '** Alternatives compare matrixes **' + '\n\n'
        for i in range(len(self.__factors)):
            result += '-----------------------------------------------------------------------------' + '\n'
            result += '* Comparing by factor ' + str(i + 1) + ': "' + self.__factors[i] + '"' + ' * \n'
            result += self.__alternatives_compare_matrixes[i].to_string() + '\n\n'
        return result
