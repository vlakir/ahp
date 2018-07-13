import argparse
import gettext


def init_dialogues():
    gettext.install('ahp_rm', './locale')


def parse_args():
    parser = argparse.ArgumentParser(
        description='''Realisation of AHP relative method by T.Saaty''',
        epilog='''(c) vlakir 2018''')
    parser.add_argument('-f', '--factors', default='factors.csv',
                        help='Path to .csv file with list of factors',
                        metavar='PATH')
    parser.add_argument('-a', '--alternatives', default='alternatives.csv',
                        help='Path to .csv file with list of alternatives',
                        metavar='PATH')
    parser.add_argument('-fc', '--factors-compare-array', default='factors_compare.csv',
                        help='Path to .csv file with factors compare array',
                        metavar='PATH')
    parser.add_argument('-ac', '--alternatives-compare-arrays', default='alternatives_compares.csv',
                        help='Path to .csv file with alternatives compare arrays',
                        metavar='PATH')
    parser.add_argument('-r', '--result', default='result.txt',
                        help='Path to .txt file with full solution expaination',
                        metavar='PATH')
    parser.add_argument('-i', '--interactive-input', action='store_const', const=True,
                        help='Ignore filepaths. All values will be asked interactively',
                        metavar='PATH')

    namespace = parser.parse_args()
    return namespace


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
    print(_("You have to enter all values manually."))


def input_factors():
    print(_("You have to enter factors manually."))
    return __input_list(_("How many factors do you want to use? "), _("Enter name of factor №"))


def input_alternatives():
    print(_("You have to enter alternatives manually."))
    return __input_list(_("How many alternatives do you want to use? "), _("Enter name of alternative №"))


def input_factors_compare(relative_measurement):

    print(_("You have to enter factors compare matrix manually."))
    __print_rate_instruction()
    factors = relative_measurement.get_factors()
    while 1:
        for i in range(1, relative_measurement.get_factors_count() + 1):
            for j in range(1, relative_measurement.get_factors_count() + 1):
                if (j - i) > 0:
                    question = _('Rate the importance of factor "%s" compared to factor "%s" [-8; 8] ') \
                               % (factors[i - 1], factors[j - 1])
                    relative_measurement.set_factors_compare_matrix_element(i, j, __input_rate(question))
        relative_measurement.calculate()
        cr = abs(relative_measurement.get_factors_compare_matrix().get_consistency_ratio())
        if not __is_normal_cr(cr):
            print('CR = %.2f' % cr)
            if __is_rerate():
                break
        else:
            break


# 2DO: CR check
def input_alternatives_compares(relative_measurement):
    print(_("You have to enter alternatives compare matrixes manually."))
    __print_rate_instruction()
    factors = relative_measurement.get_factors()
    alternatives = relative_measurement.get_alternatives()

    for k in range(relative_measurement.get_factors_count()):
        while 1:
            print(_('Compare alternatives by factor "%s"') % factors[k])
            for i in range(1, relative_measurement.get_alternatives_count() + 1):
                for j in range(1, relative_measurement.get_alternatives_count() + 1):
                    if (j - i) > 0:
                        question = _('Rate the alternative "%s" compared to the alternative "%s" [-8; 8] ') \
                                   % (alternatives[i - 1], alternatives[j - 1])
                        relative_measurement.set_alternatives_compare_matrixes_element(k + 1, i, j, __input_rate(question))
            alternatives_compare_matrix = relative_measurement.get_alternatives_compare_matrixes()[k]
            alternatives_compare_matrix.calculate()
            cr = abs(alternatives_compare_matrix.get_consistency_ratio())

            print('CR = %.2f' % cr)

            if not __is_normal_cr(cr):
                print('CR = %.2f' % cr)
                if __is_rerate():
                    break
            else:
                break


def input_yes_no(question):
    while 1:
        try:
            input_str = input(question).upper()
            local_lang_yes_upper = _('Д')
            local_lang_no_upper = _('Н')
            if input_str not in ('Y', 'N', local_lang_yes_upper, local_lang_no_upper):
                raise ValueError()
            if (input_str == 'Y') or (input_str == local_lang_yes_upper):
                return True
            else:
                return False
        except ValueError:
            print(_('You must enter only "y" or "n"! Try again. \n'))


def __is_rerate():
    return not (input_yes_no(_('There are some logical inconsistencies in your rates. Do you want to correct? (y/n) ')))


def __is_normal_cr(cr):
    if cr <= 0.2:
        return True
    else:
        return False


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
        try:
            num = int(input(question))
            if num not in (-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8):
                raise ValueError()
            if num >= 0:
                num += 1
            else:
                num = 1 / (abs(num) + 1)
            return num
        except ValueError:
            print(_('You must enter only integer number from -8 to 8! Try again. \n'))


def __print_rate_instruction():
    insruction = (_('Rating instruction:\n') +
                  _('Rate\tDefenition\n') +
                  _('0\t\tEqual preference\n') +
                  _('1\t\tSmall preference\n') +
                  _('2\t\tMedium Preference\n') +
                  _('3\t\tAbove medium preference above medium\n') +
                  _('4\t\tModerately strong preference\n') +
                  _('5\t\tStrong preference\n') +
                  _('6\t\tVery strong preference\n') +
                  _('7\t\tVery, very strong preference\n') +
                  _('8\t\tAbsolute preference\n') +
                  _('Negative values [-8 -1] correspond to the inversion of the compared entities positions\n'))
    print(insruction)
