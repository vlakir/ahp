import modules.utils as ut
import modules.matclasses as mc


def load_rm_from_csv(factor_file_path, alternatives_file_path,
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
        relative_measurement = mc.RelativeMeasurement(alternatives[0], factors[0])
        if file_checker.is_factors_compare_file_correct:
            relative_measurement.set_factors_compare_matrix_elements(factors_compare_array)
        if file_checker.is_alternatives_compares_file_correct:
            for i in range(factors_num):
                (relative_measurement.set_alternatives_compare_matrixes_elements
                 (i + 1, alternatives_compare_arrays[alternatives_num * i:alternatives_num * (i + 1)]))
    else:
        relative_measurement = None

    return relative_measurement, file_checker


def save_rm_to_csv(relative_measurement, factor_file_path, alternatives_file_path,
                   factors_compare_array_file_path, alternatives_compare_arrays_file_path):
    ut.list_to_csv(factor_file_path, [relative_measurement.get_factors()])
    ut.list_to_csv(alternatives_file_path, [relative_measurement.get_alternatives()])
    ut.list_to_csv(factors_compare_array_file_path,
                   relative_measurement.get_factors_compare_matrix().get_matrix())

    alternatives_compare_arrays = []
    alternatives_compare_matrixes = relative_measurement.get_alternatives_compare_matrixes()
    for i in range(relative_measurement.get_factors_count()):
        alternatives_compare_matrix = alternatives_compare_matrixes[i]
        for j in range(relative_measurement.get_alternatives_count()):
            row = []
            for k in range(relative_measurement.get_alternatives_count()):
                row.append(alternatives_compare_matrix.get_matrix_element(j + 1, k + 1))
            alternatives_compare_arrays.append(row)
    ut.list_to_csv(alternatives_compare_arrays_file_path, alternatives_compare_arrays)


def save_rm_string_to_file(relative_measurement, file_name):
    file = open(file_name, 'w')
    file.write(relative_measurement.to_string())


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
