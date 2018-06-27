import maimodules.matclasses as mc
import sys


try:
    relative_measurement = mc.RelativeMeasurement.make_self_from_csv('factors1.csv',
                                                                    'alternatives.csv',
                                                                    'factors_compare_array.csv',
                                                                    'alternatives_compare_arrays.csv')
except Exception as ex:
    print(ex)
    sys.exit()

relative_measurement.calculate()

print(relative_measurement.to_string())
