import modules.matclasses as mc
import modules.dialogues as dl
import modules.file_io as fio


def main():
    # fio.create_config() # uncomment if you need to reset settings.ini to default values
    args = fio.parse_args()
    dl.set_language(args.language)
    if args.interactive_input:  # no need to check and load csv-files
        dl.interactive_input_info()
        factors = dl.input_factors()
        alternatives = dl.input_alternatives()
        relative_measurement = mc.RelativeMeasurement(alternatives, factors)
        dl.input_factors_compare(relative_measurement)
        dl.input_alternatives_compares(relative_measurement)
    else:  # check and load csv-files
        relative_measurement, file_checker = (fio.load_rm_from_csv
                                              (args.path,
                                               args.factors,
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
    dl.show_result(relative_measurement)
    results_folder = fio.get_config_setting('results_folder')
    results_folder = fio.correct_last_slash_in_path(results_folder)
    fio.ensure_dir(results_folder)
    fio.save_rm_to_csv(relative_measurement,
                       results_folder + args.factors,
                       results_folder + args.alternatives,
                       results_folder + args.factors_compare_array,
                       results_folder + args.alternatives_compare_arrays)
    fio.save_rm_string_to_file(relative_measurement, results_folder, args.result)


if __name__ == '__main__':
    main()
