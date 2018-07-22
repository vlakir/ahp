import gettext
from prettytable import PrettyTable
import modules.utils as ut
import modules.file_io as fio


def set_language(language):
    """
    Set the language of the user interface using gettext module

    @param language: Language string as part of the path to messages.mo: 'en', 'ru', etc
    @type language: string
    """
    try:
        lang = gettext.translation('messages', fio.get_config_setting('locale_folder'), languages=[language])
        lang.install()
    except FileNotFoundError:
        print('File messages.mo is not found for language "' + language + '". Use default language settings.')
        lang = gettext.translation('messages', fio.get_config_setting('locale_folder'), languages=['en'])
        lang.install()


def factors_file_info(file_checker):
    """
    Print results of factors csv-file checkings: found/not found, correct/incorrect

    @param file_checker: Object with parameters of the imported csv-file
    @type file_checker: modules.file_io.FileChecker
    """
    if not file_checker.is_factor_file_found:
        print(_("Factors file is not found"))
    elif not file_checker.is_factor_file_correct:
        print(_("Factors file has incorrect format"))
    else:
        print(_("Factors file is loaded and checked"))


def alternatives_file_info(file_checker):
    """
    Print results of alternatives csv-file checkings: found/not found, correct/incorrect

    @param file_checker: Object with parameters of the imported csv-file
    @type file_checker: modules.file_io.FileChecker
    """
    if not file_checker.is_alternatives_file_found:
        print(_("Alternatives file is not found"))
    elif not file_checker.is_alternatives_file_correct:
        print(_("Alternatives file is not correct"))
    else:
        print(_("Alternatives file is loaded and checked"))


def factors_compare_file_info(file_checker):
    """
    Print results of factors compare csv-file checkings: found/not found, correct/incorrect

    @param file_checker: Object with parameters of the imported csv-file
    @type file_checker: modules.file_io.FileChecker
    """
    if not file_checker.is_factors_compare_file_found:
        print(_("Factors compare file is not found"))
    elif not file_checker.is_factors_compare_file_correct:
        print(_("Factors compare file is not correct"))
    else:
        print(_("Factors compare file is loaded and checked"))


def alternatives_compares_file_info(file_checker):
    """
    Print results of alternatives compares csv-file checkings: found/not found, correct/incorrect

    @param file_checker: Object with parameters of the imported csv-file
    @type file_checker: modules.file_io.FileChecker
    """
    if not file_checker.is_alternatives_compares_file_found:
        print(_("Alternatives compares file is not found"))
    elif not file_checker.is_alternatives_compares_file_correct:
        print(_("Alternatives compares file is not correct"))
    else:
        print(_("Alternatives compares file is loaded and checked"))


def interactive_input_info():
    """
    Print message about interactive mode of input
    """
    print(_("Interactive mode. You have to enter all values manually."))


def input_factors():
    """
    Interactive input of factors names
    @return: List of factors names
    @rtype: list
    """
    print(_("Enter factors."))
    return __input_list(_("How many factors do you want to use?") + " ", _("Enter name of factor") + ' ')


def input_alternatives():
    """
    Interactive input of alternatives names
    @return: List of alternatives names
    @rtype: list
    """
    print(_("Enter alternatives."))
    return __input_list(_("How many alternatives do you want to use?") + " ", _("Enter name of alternative") + ' ')


def input_factors_compare(relative_measurement):
    """
    Record factor rating into object
    @param relative_measurement: Object the factor rating will be recorded into which
    @type relative_measurement: modules.matclasses.RelativeMeasurement
    """
    print()
    print(_("Enter factors compare matrix."))
    __print_rate_instruction()
    factors = relative_measurement.get_factors()
    while 1:
        for i in range(1, relative_measurement.get_factors_count() + 1):
            for j in range(1, relative_measurement.get_factors_count() + 1):
                if (j - i) > 0:
                    question = (_('Rate the importance of factor "%s" compared to factor "%s"') + ': ') \
                               % (factors[i - 1], factors[j - 1])
                    relative_measurement.set_factors_compare_matrix_element(i, j, __input_rate(question))
        relative_measurement.calculate()
        if not relative_measurement.get_factors_compare_matrix().is_normal_cr():
            print('CR = %.2f' % relative_measurement.get_factors_compare_matrix().get_consistency_ratio())
            if __is_rerate():
                break
        else:
            break


def input_alternatives_compares(relative_measurement):
    """
    Record alternatives ratings into object
    @param relative_measurement: Object the alternatives ratings will be recorded into which
    @type relative_measurement: modules.matclasses.RelativeMeasurement
    """
    print()
    print(_("Enter alternatives compare matrixes."))
    __print_rate_instruction()
    factors = relative_measurement.get_factors()
    alternatives = relative_measurement.get_alternatives()

    for k in range(relative_measurement.get_factors_count()):
        while 1:
            print()
            print(_('Compare alternatives by factor "%s"') % factors[k])
            for i in range(1, relative_measurement.get_alternatives_count() + 1):
                for j in range(1, relative_measurement.get_alternatives_count() + 1):
                    if (j - i) > 0:
                        question = (_('Rate the alternative "%s" compared to the alternative "%s"') + ': ') \
                                   % (alternatives[i - 1], alternatives[j - 1])
                        relative_measurement.set_alternatives_compare_matrixes_element(k + 1, i, j,
                                                                                       __input_rate(question))
            alternatives_compare_matrix = relative_measurement.get_alternatives_compare_matrixes()[k]
            alternatives_compare_matrix.calculate()
            if not alternatives_compare_matrix.is_normal_cr():
                print('CR = %.2f' % alternatives_compare_matrix.get_consistency_ratio())
                if __is_rerate():
                    break
            else:
                break


def input_yes_no(question):
    """
    Ask user and input answer 'y' or 'n'
    @param question: Question the user should answer to which
    @type question: string
    @return: True if the answer is 'y'. False if the answer is 'n'
    @rtype: bool
    """
    while 1:
        try:
            input_str = input(question).upper()
            local_lang_yes_upper = _('Y')
            local_lang_no_upper = _('N')
            if input_str not in ('Y', 'N', local_lang_yes_upper, local_lang_no_upper):
                raise ValueError()
            if (input_str == 'Y') or (input_str == local_lang_yes_upper):
                return True
            else:
                return False
        except ValueError:
            print(_('You must enter only "y" or "n"! Try again.') + " \n")


def show_result(relative_measurement):
    """
    Print final results of the measurement
    @param relative_measurement: Object the results will be printed from
    @type relative_measurement: modules.matclasses.RelativeMeasurement
    """
    print()
    print(get_result_str(relative_measurement))
    print(_('See results.txt for more details'))
    print()


def get_result_str(relative_measurement):
    """
    Get final results of the measurement
    @param relative_measurement: Object the results will be got from
    @type relative_measurement: modules.matclasses.RelativeMeasurement
    @return: Formated table with results
    @rtype: string
    """
    result_str = _('RESULTS OF ANALYSIS:') + '\n'
    sorted_result = relative_measurement.get_sorted_result()
    th = [_('Rating'), _('Alternative'), _('Priority')]
    table = PrettyTable(th)
    for i in range(len(sorted_result)):
            table.add_row([i+1, sorted_result[i][1], round(sorted_result[i][2], 2)])
    result_str += table.get_string()
    if not relative_measurement.is_normal_cr():
        result_str += '\n' + __rm_warning()
    return result_str


def pcm_to_string(paired_comparison_matrix):
    """
    String representation of PairedComparisonMatrix object
    @param paired_comparison_matrix: Object
    @type paired_comparison_matrix: modules.matclasses.PairedComparisonMatrix
    @return: String representation of the object
    @rtype: string
    """
    weights = paired_comparison_matrix.get_weights()
    round_digits_num = int(fio.get_config_setting('round_digits_num'))
    th = ['\\']
    for i in range(1, paired_comparison_matrix.get_size() + 1):
        th.append(paired_comparison_matrix.get_category(i))
    th.append(_('Priority'))
    table = PrettyTable(th)
    bottom_str = ''
    for i in range(1, paired_comparison_matrix.get_size() + 1):
        row = [paired_comparison_matrix.get_category(i)]
        for j in range(1, paired_comparison_matrix.get_size() + 1):
            # row.append(round(paired_comparison_matrix.get_matrix_element(i, j), round_digits_num))
            row.append(ut.get_fraction(paired_comparison_matrix.get_matrix_element(i, j), round_digits_num))
        row.append(round(weights[i - 1], round_digits_num))
        table.add_row(row)
        bottom_str = ('\n' + _('Main eigenvalue = ') +
                      str(round(paired_comparison_matrix.get_main_eigenvalue(), round_digits_num)) + '\n' +
                      'CR = '
                      + str(round(paired_comparison_matrix.get_consistency_ratio(), round_digits_num)) + '\n')

        if not paired_comparison_matrix.is_normal_cr():
            bottom_str += __rm_warning()
    return table.get_string() + bottom_str


def rm_to_string(relative_measurement):
    """
    String representation of the RelativeMeasurement object
    @param relative_measurement: Object
    @type relative_measurement: modules.matclasses.RelativeMeasurement
    @return: String representation of the object
    @rtype: string
    """
    round_digits_num = int(fio.get_config_setting('round_digits_num'))
    round_result = relative_measurement.get_sorted_result()
    for i in range(len(relative_measurement.get_alternatives())):
        round_result[i][2] = round(round_result[i][2], round_digits_num)
    result = ''
    result += _('Factors compare matrix') + '\n'
    result += relative_measurement.get_factors_compare_matrix().to_string() + '\n'
    result += _('Alternatives compare matrixes') + '\n\n'
    alternatives_compare_matrixes = relative_measurement.get_alternatives_compare_matrixes()
    factors = relative_measurement.get_factors()
    for i in range(len(factors)):
        result += _('Comparing by factor:') + ' "' + factors[i] + '"\n'
        result += alternatives_compare_matrixes[i].to_string() + '\n'
    result += get_result_str(relative_measurement)
    return result


def __rm_warning():
    """
    Warning about abnormal value of CR coefficient
    @return: Warning message
    @rtype: string
    """
    return (_('WARNING! CR has an abnormal value.') + '\n' +
            _('There are some logical inconsistencies in your rates.') + '\n')


def __is_rerate():
    """
    Ask user does he want to input rating agayn
    @return: True if user wants to rate agayn, False if he doesn't
    @rtype: bool
    """
    return not (input_yes_no(__rm_warning() + _('Do you want to rerate? (y/n)') + ' '))


def __input_list(len_question, enter_sentence):
    """
    Input list of factors or alternatives
    @param len_question: Question about quantity of members
    @type len_question: string
    @param enter_sentence: Suggestion to enter a next value
    @type enter_sentence: string
    @return: Factors or alternatives
    @rtype: list
    """
    while 1:
        try:
            num = int(input(len_question))
            if num < 1:
                raise ValueError()
            result = []
            for i in range(num):
                result.append(input(enter_sentence + str(i + 1) + ": "))
            return result
        except ValueError:
            print(_('You must enter only positive integer number! Try again.') + '\n')


def __input_rate(enter_sentence):
    """
    Input value of the rate
    @param enter_sentence: Suggestion to enter a value
    @type enter_sentence: string
    @return: Value of the rate
    @rtype: float
    """
    while 1:
        num_str = input(enter_sentence)
        try:
            num = int(num_str)
            if num in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                return num
            else:
                raise ValueError()
        except ValueError:
            num_list = num_str.split('/')
            try:
                if len(num_list) != 2:
                    raise ValueError()
                else:
                    numerator = int(num_list[0])
                    denominator = int(num_list[1])
                    if (numerator != 1) or (denominator < 2) or (denominator > 9):
                        raise ValueError()
                    else:
                        num = numerator / denominator
                        return num
            except ValueError:
                print(_('You must enter integer number from 1 to 9 or simple fraction from 1/9 to 1/2') + '\n' +
                      _('Try again.') + '\n')


def __print_rate_instruction():
    """
    Print instruction about values of rates
    """
    print('\n' + _('RATING INSTRUCTION:'))
    th = [_('Definition'), _('Rate')]
    table = PrettyTable(th)
    table.add_row([_('Absolute advantage'), '9'])
    table.add_row([_('Very, very strong advantage'), '8'])
    table.add_row([_('Very strong advantage'), '7'])
    table.add_row([_('Strong advantage'), '6'])
    table.add_row([_('Moderately strong advantage'), '5'])
    table.add_row([_('Above medium advantage'), '4'])
    table.add_row([_('Medium advantage'), '3'])
    table.add_row([_('Small advantage'), '2'])
    table.add_row([_('Equivalence'), '1'])
    table.add_row([_('Small disadvantage'), '1/2'])
    table.add_row([_('Medium disadvantage'), '1/3'])
    table.add_row([_('Above medium disadvantage'), '1/4'])
    table.add_row([_('Moderately strong disadvantage'), '1/5'])
    table.add_row([_('Strong disadvantage'), '1/6'])
    table.add_row([_('Very strong disadvantage'), '1/7'])
    table.add_row([_('Very, very strong disadvantage'), '1/8'])
    table.add_row([_('Absolute disadvantage'), '1/9'])
    print(str(table) + '\n')


if __name__ == '__main__':
    print('This module is intended only for import, not for execution!')
