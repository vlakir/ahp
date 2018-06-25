import maimodules.matclasses as mc


relative_measurement = mc.make_relative_measurement_from_csv('factors.csv',
                                                             'alternatives.csv',
                                                             'factors_compare_array.csv',
                                                             'alternatives_compare_arrays.csv')

relative_measurement.calculate()

print(relative_measurement.to_string())
