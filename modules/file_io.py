import modules.utils as ut
import modules.matclasses as mc
import argparse
import configparser
import csv
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description='''Realisation of AHP relative method by T.Saaty''',
        epilog='''(c) vlakir 2018''')
    parser.add_argument('-p', '--path', default='.\\',
                        help='Path to input files',
                        metavar='PATH')
    parser.add_argument('-f', '--factors', default='factors.csv',
                        help='Name of .csv file with list of factors',
                        metavar='NAME')
    parser.add_argument('-a', '--alternatives', default='alternatives.csv',
                        help='Name of  .csv file with list of alternatives',
                        metavar='NAME')
    parser.add_argument('-fc', '--factors-compare-array', default='factors_compare.csv',
                        help='Name of .csv file with factors compare array',
                        metavar='NAME')
    parser.add_argument('-ac', '--alternatives-compare-arrays', default='alternatives_compares.csv',
                        help='Name of .csv file with alternatives compare arrays',
                        metavar='NAME')
    parser.add_argument('-r', '--result', default='result.txt',
                        help='Name of .txt file with full solution expaination',
                        metavar='NAME')
    parser.add_argument('-i', '--interactive-input', action='store_const', const=True,
                        help='Ignore filepaths. All values will be asked interactively')
    parser.add_argument('-l', '--language', default='en',
                        help='Language of user intreface: en, ru etc',
                        metavar='LANGUAGE')
    namespace = parser.parse_args()
    return namespace


def load_rm_from_csv(path, factor_file_name, alternatives_file_name,
                     factors_compare_array_file_name, alternatives_compare_arrays_file_name):
    file_checker = FileChecker()

    try:
        factors = csv_to_list(correct_last_slash_in_path(path) + factor_file_name)
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
        alternatives = csv_to_list(correct_last_slash_in_path(path) + alternatives_file_name)
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
        factors_compare_array = ut.str_list_to_float(csv_to_list(correct_last_slash_in_path(path) +
                                                                 factors_compare_array_file_name))
        file_checker.is_factors_compare_file_found = True
        file_checker.is_factors_compare_file_correct = ((len(factors_compare_array) == factors_num)
                                                        and (len(factors_compare_array[0]) == factors_num))
    except FileNotFoundError:
        file_checker.is_factors_compare_file_found = False
        file_checker.is_factors_compare_file_correct = False
        factors_compare_array = []

    try:
        alternatives_compare_arrays = ut.str_list_to_float(csv_to_list(correct_last_slash_in_path(path) +
                                                                       alternatives_compare_arrays_file_name))
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
    list_to_csv(factor_file_path, [relative_measurement.get_factors()])
    list_to_csv(alternatives_file_path, [relative_measurement.get_alternatives()])
    list_to_csv(factors_compare_array_file_path, relative_measurement.get_factors_compare_matrix().get_matrix())

    alternatives_compare_arrays = []
    alternatives_compare_matrixes = relative_measurement.get_alternatives_compare_matrixes()
    for i in range(relative_measurement.get_factors_count()):
        alternatives_compare_matrix = alternatives_compare_matrixes[i]
        for j in range(relative_measurement.get_alternatives_count()):
            row = []
            for k in range(relative_measurement.get_alternatives_count()):
                row.append(alternatives_compare_matrix.get_matrix_element(j + 1, k + 1))
            alternatives_compare_arrays.append(row)
        list_to_csv(alternatives_compare_arrays_file_path, alternatives_compare_arrays)


def save_rm_string_to_file(relative_measurement, path, file_name):
    path = correct_last_slash_in_path(path)
    ensure_dir(path)
    file = open(path + file_name, 'w')
    file.write(relative_measurement.to_string())


def create_config():
    config = configparser.ConfigParser()
    config.add_section('Settings')
    config.set('Settings', 'results_folder', './results')
    config.set('Settings', 'locale_folder', './locale')
    config.set('Settings', 'round_digits_num', '3')
    with open('settings.ini', 'w') as config_file:
        config.write(config_file)


def get_config_setting(setting_name):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    return config.get("Settings", setting_name)


def ensure_dir(path):
    """
    Create the folder if it's not exist
    @param path: Path including folder name
    @type path: string
    """
    path = correct_last_slash_in_path(path)
    directory = os.path.dirname(path)
    if not directory == '':
        if not os.path.exists(directory):
            os.makedirs(directory)


def csv_to_list(file_path):
    """
    Import from csv-file to list
    @param file_path: Path to the csv file (including its name)
    @type file_path: string
    @return: Imported values
    @rtype: list
    """
    with open(file_path, newline='', encoding='utf-8') as file_obj:
        reader = csv.reader(file_obj)
        result = list(reader)
    return result


def list_to_csv(file_path, list_to_write):
    """
    Export from list to csv file
    @param file_path: Path to the csv file (including its name)
    @type file_path: string
    @param list_to_write: Values to export
    @type list_to_write: list
    """
    with open(file_path, "w", newline='', encoding='utf-8') as file_obj:
        writer = csv.writer(file_obj, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        # print(list_to_write)
        for line in list_to_write:
            writer.writerow(line)


def correct_last_slash_in_path(path):
    if path[-1] != '/' and path[-1] != '\\':
        return path + '/'
    else:
        return path


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


if __name__ == '__main__':
    print('This module is intended only for import, not for execution!')
