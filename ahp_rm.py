import maimodules.matclasses as mc
import argparse

parser = argparse.ArgumentParser(
    description='''Realisation of AHP relative method by T.Saaty''',
    epilog='''(c) vlakir 2018''')

parser.add_argument('-f', '--factors',
                    help='Path to .csv file with list of factors',
                    metavar='PATH')
parser.add_argument('-a', '--alternatives',
                    help='Path to .csv file with list of alternatives',
                    metavar='PATH')
parser.add_argument('-fc', '--factors-compare-array',
                    help='Path to .csv file with factors compare array',
                    metavar='PATH')
parser.add_argument('-ac', '--alternatives-compare-arrays',
                    help='Path to .csv file with alternatives compare arrays',
                    metavar='PATH')

namespace = parser.parse_args()

(relative_measurement, file_checker) = (mc.RelativeMeasurement.load_from_csv
                                        (str(namespace.factors),
                                         str(namespace.alternatives),
                                         str(namespace.factors_compare_array),
                                         str(namespace.alternatives_compare_arrays)))
if not file_checker.is_factor_file_found:
    print("Factors file is not found")
    # 2DO: вводим интерактивно
elif not file_checker.is_factor_file_correct:
    print("Factors file is not correct")
    # 2DO: вводим интерактивно
else:
    print("Factors file is loaded and checked")

if not file_checker.is_alternatives_file_found:
    print("Alternatives file is not found")
    # 2DO: вводим интерактивно
elif not file_checker.is_alternatives_file_correct:
    print("Alternatives file is not correct")
    # 2DO: вводим интерактивно
else:
    print("Alternatives file is loaded and checked")

if not file_checker.is_factors_compare_file_found:
    print("Factors compare file is not found")
    # 2DO: вводим интерактивно
elif not file_checker.is_factors_compare_file_correct:
    print("Factors compare file is not correct")
    # 2DO: вводим интерактивно
else:
    print("Factors compare file is loaded and checked")

if not file_checker.is_alternatives_compares_file_found:
    print("Alternatives compares file is not found")
    # 2DO: вводим интерактивно
elif not file_checker.is_alternatives_compares_file_correct:
    print("Alternatives compares file is not correct")
    # 2DO: вводим интерактивно
else:
    print("Alternatives compares file is loaded and checked")

if relative_measurement is not None:
    print("Loaded from csv-files data is enough")
    relative_measurement.calculate()
    print(relative_measurement.get_sorted_result())
    relative_measurement.save_to_csv('factors_result.csv',
                                     'alternatives_result.csv',
                                     'factors_compare_array_result.csv',
                                     'alternatives_compare_arrays_result.csv')
else:
    print("Loaded from csv-files data is NOT enough")
