import numpy as np
import maimodules.utils as ut
import maimodules.dialogues as dl


class PairedComparisonMatrix(object):

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
            if not value == 0:
                self.__matrix[column_num - 1, row_num - 1] = 1 / value
            else:
                self.__matrix[column_num - 1, row_num - 1] = 0

    def get_matrix_element(self, row_num, column_num):
        return self.__matrix[row_num - 1, column_num - 1]

    def set_matrix(self, array):
        for i in range(self.__n):
            for j in range(self.__n):
                self.set_matrix_element(i + 1, j + 1, array[i][j])

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

    def get_main_eigenvector(self):
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

    def get_unsorted_result(self):
        return ut.glue_result(self.__categories, self.get_weights(), False)

    def get_sorted_result(self):
        return ut.glue_result(self.__categories, self.get_weights(), True)

    def to_string(self):
        return dl.pcm_to_string(self)

    def string_to_file(self, file_name):
        file = open(file_name, 'w')
        file.write(self.to_string())


class RelativeMeasurement(object):
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
        return self.__factors_compare_matrix

    def get_alternatives_compare_matrixes(self):
        return self.__alternatives_compare_matrixes

    def get_factors_count(self):
        return len(self.__factors)

    def get_alternatives_count(self):
        return len(self.__alternatives)

    def get_factors(self):
        return self.__factors

    def get_alternatives(self):
        return self.__alternatives

    def set_factors_compare_matrix_element(self, row_num, column_num, value):
        self.__factors_compare_matrix.set_matrix_element(row_num, column_num, value)

    def set_alternatives_compare_matrixes_element(self, matrix_num, row_num, column_num, value):
        self.__alternatives_compare_matrixes[matrix_num - 1].set_matrix_element(row_num, column_num, value)

    def set_factors_compare_matrix_elements(self, array):
        self.__factors_compare_matrix.set_matrix(array)

    def set_alternatives_compare_matrixes_elements(self, matrix_num, array):
        self.__alternatives_compare_matrixes[matrix_num - 1].set_matrix(array)

    def get_weights(self):
        return self.get_weights()

    def calculate(self):
        self.__factors_compare_matrix.calculate()
        for i in range(len(self.__factors)):
            self.__alternatives_compare_matrixes[i].calculate()

        for i in range(len(self.__alternatives)):
            for j in range(len(self.__factors)):
                self.__weights[i] += (self.__alternatives_compare_matrixes[j].get_weights()[i] *
                                      self.__factors_compare_matrix.get_weights()[j])

    def get_unsorted_result(self):
        return ut.glue_result(self.__alternatives, self.__weights, False)

    def get_sorted_result(self):
        return ut.glue_result(self.__alternatives, self.__weights, True)

    @staticmethod
    def load_from_csv(factor_file_path, alternatives_file_path,
                      factors_compare_array_file_path, alternatives_compare_arrays_file_path):

        file_checker = FileChecker()

        try:
            factors = ut.csv_to_list(factor_file_path)
            file_checker.is_factor_file_found = True
            file_checker.is_factor_file_correct = (len(factors) == 1)
            if file_checker.is_factor_file_correct:
                factors_num = len(factors[0])
            else:
                factors_num = 0
                factors = []
        except FileNotFoundError:
            file_checker.is_factor_file_found = False
            file_checker.is_factor_file_correct = False
            factors_num = 0
            factors = []

        try:
            alternatives = ut.csv_to_list(alternatives_file_path)
            file_checker.is_alternatives_file_found = True
            file_checker.is_alternatives_file_correct = (len(alternatives) == 1)
            if file_checker.is_alternatives_file_correct:
                alternatives_num = len(alternatives[0])
            else:
                alternatives_num = 0
                alternatives = []
        except FileNotFoundError:
            file_checker.is_alternatives_file_found = False
            file_checker.is_alternatives_file_correct = False
            alternatives_num = 0
            alternatives = []

        try:
            factors_compare_array = ut.str_list_to_float(ut.csv_to_list(factors_compare_array_file_path))
            file_checker.is_factors_compare_file_found = True
            file_checker.is_factors_compare_file_correct = ((len(factors_compare_array) == factors_num)
                                                            and (len(factors_compare_array[0]) == factors_num))
        except FileNotFoundError:
            file_checker.is_factors_compare_file_found = False
            file_checker.is_factors_compare_file_correct = False
            factors_compare_array = []

        try:
            alternatives_compare_arrays = ut.str_list_to_float(ut.csv_to_list(alternatives_compare_arrays_file_path))
            file_checker.is_alternatives_compares_file_found = True
            file_checker.is_alternatives_compares_file_correct = ((len(alternatives_compare_arrays) ==
                                                                  factors_num * alternatives_num)
                                                                  and (len(alternatives_compare_arrays[0]) ==
                                                                  alternatives_num))
        except FileNotFoundError:
            file_checker.is_alternatives_compares_file_found = False
            file_checker.is_alternatives_compares_file_correct = False
            alternatives_compare_arrays = []

        if file_checker.is_factor_file_correct and file_checker.is_alternatives_file_correct:
            relative_measurement = RelativeMeasurement(alternatives[0], factors[0])
            if file_checker.is_factors_compare_file_correct:
                relative_measurement.set_factors_compare_matrix_elements(factors_compare_array)
            if file_checker.is_alternatives_compares_file_correct:
                for i in range(factors_num):
                    (relative_measurement.set_alternatives_compare_matrixes_elements
                     (i + 1, alternatives_compare_arrays[alternatives_num * i:alternatives_num * (i + 1)]))
        else:
            relative_measurement = None

        return relative_measurement, file_checker

    def save_to_csv(self, factor_file_path, alternatives_file_path,
                    factors_compare_array_file_path, alternatives_compare_arrays_file_path):
        ut.list_to_csv(factor_file_path, [self.get_factors()])
        ut.list_to_csv(alternatives_file_path, [self.get_alternatives()])
        ut.list_to_csv(factors_compare_array_file_path,
                       self.get_factors_compare_matrix().get_matrix())

        alternatives_compare_arrays = []
        alternatives_compare_matrixes = self.get_alternatives_compare_matrixes()
        for i in range(self.get_factors_count()):
            alternatives_compare_matrix = alternatives_compare_matrixes[i]
            for j in range(self.get_alternatives_count()):
                row = []
                for k in range(self.get_alternatives_count()):
                    row.append(alternatives_compare_matrix.get_matrix_element(j + 1, k + 1))
                alternatives_compare_arrays.append(row)
        ut.list_to_csv(alternatives_compare_arrays_file_path, alternatives_compare_arrays)

    def to_string(self):
        return dl.rm_to_string(self)

    def string_to_file(self, file_name):
        file = open(file_name, 'w')
        file.write(self.to_string())


class FileChecker(object):
    def __init__(self):
        self.is_factor_file_found = False
        self.is_factor_file_correct = False
        self.is_alternatives_file_found = False
        self.is_alternatives_file_correct = False
        self.is_factors_compare_file_found = False
        self.is_factors_compare_file_correct = False
        self.is_alternatives_compares_file_found = False
        self.is_alternatives_compares_file_correct = False
