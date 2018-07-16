import gettext
from prettytable import PrettyTable


def set_language(language):
    try:
        lang = gettext.translation('messages', './locale', languages=[language])
        lang.install()
    except FileNotFoundError:
        print('File messages.mo is not found for language "' + language + '". Use default language settings.')
        lang = gettext.translation('messages', './locale', languages=['en'])
        lang.install()


def factors_file_info(file_checker):
    if not file_checker.is_factor_file_found:
        print(_("Factors file is not found."))
    elif not file_checker.is_factor_file_correct:
        print(_("Factors file is not correct."))
    else:
        print(_("Factors file is loaded and checked"))


def alternatives_file_info(file_checker):
    if not file_checker.is_alternatives_file_found:
        print(_("Alternatives file is not found"))
    elif not file_checker.is_alternatives_file_correct:
        print(_("Alternatives file is not correct"))
    else:
        print(_("Alternatives file is loaded and checked"))


def factors_compare_file_info(file_checker):
    if not file_checker.is_factors_compare_file_found:
        print(_("Factors compare file is not found"))
    elif not file_checker.is_factors_compare_file_correct:
        print(_("Factors compare file is not correct"))
    else:
        print(_("Factors compare file is loaded and checked"))


def alternatives_compares_file_info(file_checker):
    if not file_checker.is_alternatives_compares_file_found:
        print(_("Alternatives compares file is not found"))
    elif not file_checker.is_alternatives_compares_file_correct:
        print(_("Alternatives compares file is not correct"))
    else:
        print(_("Alternatives compares file is loaded and checked"))


def interactive_input_info():
    print(_("Interactive mode. You have to enter all values manually."))


def input_factors():
    print(_("Enter factors."))
    return __input_list(_("How many factors do you want to use?") + " ", _("Enter name of factor №"))


def input_alternatives():
    print(_("Enter alternatives."))
    return __input_list(_("How many alternatives do you want to use?") + " ", _("Enter name of alternative №"))


def input_factors_compare(relative_measurement):
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
            print(_('You must enter only "y" or "n"! Try again. \n'))


def show_result(relative_measurement):
    print()
    print(get_result_str(relative_measurement))
    print(_('See results.txt for more details'))
    print()


def get_result_str(relative_measurement):
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
    weights = paired_comparison_matrix.get_weights()
    round_digits_num = 3
    th = ['\\']
    for i in range(1, paired_comparison_matrix.get_size() + 1):
        th.append(paired_comparison_matrix.get_category(i))
    th.append(_('Priority'))
    table = PrettyTable(th)
    bottom_str = ''
    for i in range(1, paired_comparison_matrix.get_size() + 1):
        row = [paired_comparison_matrix.get_category(i)]
        for j in range(1, paired_comparison_matrix.get_size() + 1):
            row.append(round(paired_comparison_matrix.get_matrix_element(i, j), round_digits_num))
        row.append(round(weights[i - 1], round_digits_num))
        table.add_row(row)
        bottom_str = ('\n' + _('Main eigenvalue = ') +
                      str(round(paired_comparison_matrix.get_main_eigenvalue(), round_digits_num)) + '\n' +
                      'C.R. = '
                      + str(round(paired_comparison_matrix.get_consistency_ratio(), round_digits_num)) + '\n')

        if not paired_comparison_matrix.is_normal_cr():
            bottom_str += __rm_warning()
    return table.get_string() + bottom_str


def rm_to_string(relative_measurement):
    round_digits_num = 3
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
        result += _('Comparing by factor: "') + factors[i] + '"\n'
        result += alternatives_compare_matrixes[i].to_string() + '\n'
    result += get_result_str(relative_measurement)
    return result


def __rm_warning():
    return _('WARNING! CR has an abnormal value.') + '\n' + \
           _('There are some logical inconsistencies in your rates.') + '\n'


def __is_rerate():
    return not (input_yes_no(__rm_warning() + _('Do you want to rerate? (y/n)') + ' '))


def __input_list(len_question, enter_sentence):
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
            print(_('You must enter only positive integer number! Try again. \n'))


def __input_rate(question):
    while 1:
        num_str = input(question)
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
    print()
    print(_('RATING INSTRUCTION:'))
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
    table.add_row([_('Equal'), '1'])
    table.add_row([_('Small disadvantage'), '1/2'])
    table.add_row([_('Medium disadvantage'), '1/3'])
    table.add_row([_('Above medium disadvantage'), '1/4'])
    table.add_row([_('Moderately strong disadvantage'), '1/5'])
    table.add_row([_('Strong disadvantage'), '1/6'])
    table.add_row([_('Very strong disadvantage'), '1/7'])
    table.add_row([_('Very, very strong disadvantage'), '1/8'])
    table.add_row([_('Absolute disadvantage'), '1/9'])
    print(table)
    print()
