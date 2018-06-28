import maimodules.matclasses as mc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--factors')
parser.add_argument('-a', '--alternatives')
parser.add_argument('-fc', '--factors_compare_array')
parser.add_argument('-ac', '--alternatives_compare_arrays')

namespace = parser.parse_args()

(relative_measurement, file_checker) = (mc.RelativeMeasurement.make_self_from_csv
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
else:
    print("Loaded from csv-files data is NOT enough")
