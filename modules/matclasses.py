import numpy as np
import modules.utils as ut
import modules.dialogues as dl


class PairedComparisonMatrix(object):
    """
    Container for comparison  matrix for set of named categories
    """

    def __init__(self, size):
        self.__n = size
        # noinspection PyUnresolvedReferences
        self.__matrix = np.zeros(shape=(self.__n, self.__n))
        for i in range(self.__n):
            self.__matrix[i, i] = 1
        self.__categories = [''] * self.__n
        self.__main_eigenvalue = 0
        # noinspection PyUnresolvedReferences
        self.__main_eigenvector = np.zeros(shape=self.__n)

    def set_matrix_element(self, row_idx, column_idx, value):
        """
        Set single matrix member
        :param row_idx: Index of row (numbering from 1, not from 0!)
        :type row_idx: int
        :param column_idx: Number of column (numbering from 1, not from 0!)
        :type column_idx: int
        :param value: setted value
        :type value: float
        """
        if row_idx == column_idx:
            self.__matrix[row_idx - 1, column_idx - 1] = 1
        else:
            self.__matrix[row_idx - 1, column_idx - 1] = value
            if not value == 0:
                self.__matrix[column_idx - 1, row_idx - 1] = 1 / value
            else:
                self.__matrix[column_idx - 1, row_idx - 1] = 0

    def get_matrix_element(self, row_idx, column_idx):
        """
        Get single matrix member
        :param row_idx: Index of row (numbering from 1, not from 0!)
        :type row_idx: int
        :param column_idx: Index of column (numbering from 1, not from 0!)
        :type column_idx: int
        :return: value of matrix member
        :rtype: float
        """
        return self.__matrix[row_idx - 1, column_idx - 1]

    def set_matrix_elements(self, array):
        """
        Set all matrix members from list
        :param array: Square array of matrix members
        :type array: list[][]
        """
        for i in range(self.__n):
            for j in range(self.__n):
                self.set_matrix_element(i + 1, j + 1, array[i][j])

    def get_matrix(self):
        """
        Get all matrix members as list
        :return: Square array of matrix members
        :rtype: list
        """
        return self.__matrix

    def set_category(self, idx, value):
        """
        Set name of categorie
        :param idx: Index of categorie (numbering from 1, not from 0!)
        :type idx: int
        :param value: setted value
        :type value: string
        """
        self.__categories[idx - 1] = value

    def get_category(self, idx):
        """
        Get name of categorie
        :param idx: Index of categorie (numbering from 1, not from 0!)
        :type idx: int
        :return: Name of categorie
        :rtype: string
        """
        return self.__categories[idx - 1]

    def set_categories(self, array):
        """
        Set all categories names from list
        :param array: Categories names
        :type array: list
        """
        for i in range(self.__n):
            self.set_category(i, array[i - 1])

    def get_categories(self):
        """
        Get all categories names as list
        :return: Categories names
        :rtype: list
        """
        return self.__categories

    def get_size(self):
        """
        Get size of square matrix
        :return: Size
        :rtype: int
        """
        return self.__n

    def calculate(self):
        """
        Calculate main eigenvector, main eigenvalue and weigts for a given matrix
        """
        v, w = np.linalg.eig(self.__matrix)
        v = abs(v)
        w = abs(w)
        perron_position = np.argmax(v)
        self.__main_eigenvalue = v[perron_position]
        self.__main_eigenvector = w[:, perron_position]

    def get_main_eigenvalue(self):
        """
        Get main eigenvector. Run this method only after calculate()
        :return: Main eigenvalue of matrix
        :rtype: float
        """
        return self.__main_eigenvalue

    def get_main_eigenvector(self):
        """
        Get main eigenvector. Run this method only after calculate()
        :return: Main eigenvector of matrix
        :rtype: float
        """
        return self.__main_eigenvector

    def get_weights(self):
        """
        Get vector of weigths. Run this method only after calculate()
        :return: Vector of weigths
        :rtype: list
        """
        summa = sum(self.__main_eigenvector)
        if summa != 0:
            result = self.__main_eigenvector / summa
        else:
            result = self.__main_eigenvector * 0
        return result

    def get_consistency_index(self):
        """
        Get CI coefficient. Run this method only after calculate()
        :return: CI coefficient
        :rtype: float
        """
        return (self.__main_eigenvalue - self.__n) / (self.__n - 1)

    def get_consistency_ratio(self):
        """
        Get CR coefficient. Run this method only after calculate()
        :return: CR coefficient
        :rtype: float
        """
        n_to_ri = {
            1: 0.01,
            2: 0.01,
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

    def is_normal_cr(self):
        """
        Check is CR has normal value (positiv and <= 0.2)
        :return: Result of checking
        :rtype: bool
        """
        if (self.get_consistency_ratio() <= 0.2) and (self.get_consistency_ratio() >= 0):
            return True
        else:
            return False

    def get_unsorted_result(self):
        """
        Get result of calculation where categories sorted by their indexes
        :return: [[Index, name of categorie, weight], ...]
        :rtype: list[][]
        """
        return ut.glue_result(self.__categories, self.get_weights(), False)

    def get_sorted_result(self):
        """
        Get result of calculation where categories sorted by their weights
        :return: [[Index, name of categorie, weight], ...]
        :rtype: list[][]
        """
        return ut.glue_result(self.__categories, self.get_weights(), True)

    def to_string(self):
        """
        Get string representation of the object
        :return: String representation of the object
        :rtype: string
        """
        return dl.pcm_to_string(self)


class RelativeMeasurement(object):
    """
    Container for all measurement data
    """
    def __init__(self, alternatives, factors):
        self.__factors = factors
        self.__alternatives = alternatives
        self.__factors_compare_matrix = PairedComparisonMatrix(len(factors))
        self.__factors_compare_matrix.set_categories(self.__factors)
        self.__weights = [0] * len(self.__alternatives)
        self.__alternatives_compare_matrixes = []
        for i in range(len(factors)):
            acm = PairedComparisonMatrix(len(alternatives))
            acm.set_categories(self.__alternatives)
            self.__alternatives_compare_matrixes.append(acm)

    def get_factors_compare_matrix(self):
        """
        Get matrix of factors compare
        :return: Matrix of factors compare
        :rtype: modules.PairedComparisonMatrix
        """
        return self.__factors_compare_matrix

    def get_alternatives_compare_matrixes(self):
        """
        Get matrixes of alternatives compare
        :return: Matrixes of alternatives compare
        :rtype: modules.PairedComparisonMatrix[]
        """
        return self.__alternatives_compare_matrixes

    def get_factors_count(self):
        """
        Get count of factors
        :return: Count of factors
        :rtype: int
        """
        return len(self.__factors)

    def get_alternatives_count(self):
        """
        Get count of alternatives
        :return: Count of alternatives
        :rtype: int
        """
        return len(self.__alternatives)

    def get_factors(self):
        """
        Get factors names
        :return: Factors names
        :rtype: list
        """
        return self.__factors

    def get_alternatives(self):
        """
        Get alternatives names
        :return: Alternatives names
        :rtype: list
        """
        return self.__alternatives

    def set_factors_compare_matrix_element(self, row_idx, column_idx, value):
        """
        Set single factors compare matrix member
        :param row_idx: Index of row (numbering from 1, not from 0!)
        :type row_idx: int
        :param column_idx: Number of column (numbering from 1, not from 0!)
        :type column_idx: int
        :param value: setted value
        :type value: float
        """
        self.__factors_compare_matrix.set_matrix_element(row_idx, column_idx, value)

    def set_alternatives_compare_matrixes_element(self, factor_idx, row_idx, column_idx, value):
        """
        Set single alternatives compare matrix member
        :param factor_idx: Index of factor (numbering from 1, not from 0!)
        :type factor_idx: int
        :param row_idx: Index of row (numbering from 1, not from 0!)
        :type row_idx: int
        :param column_idx: Number of column (numbering from 1, not from 0!)
        :type column_idx: int
        :param value: setted value
        :type value: float
        """
        self.__alternatives_compare_matrixes[factor_idx - 1].set_matrix_element(row_idx, column_idx, value)

    def set_factors_compare_matrix_elements(self, array):
        """
        Set all factors compare matrix members from list
        :param array: Square array of matrix members
        :type array: list[][]
        """
        self.__factors_compare_matrix.set_matrix_elements(array)

    def set_alternatives_compare_matrixes_elements(self, factor_idx, array):
        """
        Set all alternatives compare matrix members for selected factor index from list
        :param factor_idx: Index of factor (numbering from 1, not from 0!)
        :type factor_idx: int
        :param array: Square array of matrix members
        :type array: list[][]
        """
        self.__alternatives_compare_matrixes[factor_idx - 1].set_matrix_elements(array)

    def get_weights(self):
        """
        Get vector of weigths. Run this method only after calculate()
        :return: Vector of weigths
        :rtype: list
        """
        return self.get_weights()

    def calculate(self):
        """
        Calculate main eigenvectors, main eigenvalues and weigts for all matrixes
        """
        self.__factors_compare_matrix.calculate()
        for i in range(len(self.__factors)):
            self.__alternatives_compare_matrixes[i].calculate()

        for i in range(len(self.__alternatives)):
            for j in range(len(self.__factors)):
                self.__weights[i] += (self.__alternatives_compare_matrixes[j].get_weights()[i] *
                                      self.__factors_compare_matrix.get_weights()[j])

    def get_unsorted_result(self):
        """
        Get result of calculation where alternatives sorted by their indexes
        :return: [[Index, name of alternative, weight], ...]
        :rtype: list[][]
        """
        return ut.glue_result(self.__alternatives, self.__weights, False)

    def get_sorted_result(self):
        """
        Get result of calculation where alternatives sorted by their weights
        :return: [[Index, name of alternative, weight], ...]
        :rtype: list[][]
        """
        return ut.glue_result(self.__alternatives, self.__weights, True)

    def is_normal_cr(self):
        """
        Check is all CRs have normal values (positiv and <= 0.2)
        :return: Result of checking
        :rtype: bool
        """
        result = self.get_factors_compare_matrix().is_normal_cr()
        for i in range(self.get_alternatives_count()):
            result = (result and self.get_alternatives_compare_matrixes()[i].is_normal_cr())
        return result

    def to_string(self):
        """
        Get string representation of the object
        :return: String representation of the object
        :rtype: string
        """
        return dl.rm_to_string(self)


if __name__ == '__main__':
    print('This module is intended only for import, not for execution!')
