import maimodules.matclasses as mc
import maimodules.dialogues as dl


args = dl.parse_args()

if args.interactive_input:
    relative_measurement, file_checker = (mc.RelativeMeasurement.load_from_csv
                                          ('',
                                           '',
                                           '',
                                           ''))
    dl.interactive_input_info()
    factors = dl.input_factors()
    alternatives = dl.input_alternatives()
    relative_measurement = mc.RelativeMeasurement(alternatives, factors)

    dl.input_factors_compare(relative_measurement)
    dl.input_alternatives_compares(relative_measurement)

else:
    relative_measurement, file_checker = (mc.RelativeMeasurement.load_from_csv
                                          (args.factors,
                                           args.alternatives,
                                           args.factors_compare_array,
                                           args.alternatives_compare_arrays))
    dl.factors_file_info(file_checker)
    dl.alternatives_file_info(file_checker)

    if relative_measurement is None:
        factors = dl.input_factors()
        alternatives = dl.input_alternatives()
        relative_measurement = mc.RelativeMeasurement(alternatives, factors)
        dl.input_factors_compare(relative_measurement)
        dl.input_alternatives_compares(relative_measurement)
    else:
        dl.factors_compare_file_info(file_checker)
        if not file_checker.is_factors_compare_file_correct:
            dl.input_factors_compare(relative_measurement)

        dl.alternatives_compares_file_info(file_checker)
        if not file_checker.is_alternatives_compares_file_correct:
            dl.input_alternatives_compares(relative_measurement)


relative_measurement.calculate()
print(relative_measurement.get_sorted_result())
relative_measurement.save_to_csv('result_' + args.factors,
                                 'result_' + args.alternatives,
                                 'result_' + args.factors_compare_array,
                                 'result_' + args.alternatives_compare_arrays)

relative_measurement.string_to_file(args.result)

