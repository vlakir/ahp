import maimodules.matclasses as mc


(relative_measurement,
 is_factor_file_found,
 is_factor_file_correct,
 is_alternatives_file_found,
 is_alternatives_file_correct,
 is_factors_compare_file_found,
 is_factors_compare_file_correct,
 is_alternatives_compares_file_found,
 is_alternatives_compares_file_correct) = (mc.RelativeMeasurement.make_self_from_csv
                                          ('factors.csv',
                                           'alternatives.csv',
                                           'factors_compare_array.csv',
                                           'alternatives_compare_arrays.csv'))
if not is_factor_file_found:
    print("Factors file is not found")
    # 2DO: вводим интерактивно
elif not is_factor_file_correct:
    print("Factors file is not correct")
    # 2DO: вводим интерактивно
else:
    print("Factors file is loaded and checked")

if not is_alternatives_file_found:
    print("Alternatives file is not found")
    # 2DO: вводим интерактивно
elif not is_alternatives_file_correct:
    print("Alternatives file is not correct")
    # 2DO: вводим интерактивно
else:
    print("Alternatives file is loaded and checked")

if not is_factors_compare_file_found:
    print("Factors compare file is not found")
    # 2DO: вводим интерактивно
elif not is_factors_compare_file_correct:
    print("Factors compare file is not correct")
    # 2DO: вводим интерактивно
else:
    print("Factors compare file is loaded and checked")

if not is_alternatives_compares_file_found:
    print("Alternatives compares file is not found")
    # 2DO: вводим интерактивно
elif not is_alternatives_compares_file_correct:
    print("Alternatives compares file is not correct")
    # 2DO: вводим интерактивно
else:
    print("Alternatives compares file is loaded and checked")

if relative_measurement is not None:
    print("Loaded from csv-files data is enough")
    relative_measurement.calculate()
    # print(relative_measurement.to_string())
else:
    print("Loaded from csv-files data is NOT enough")
