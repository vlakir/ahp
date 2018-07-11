import argparse


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
        print("Factors file is not found.")
    elif not file_checker.is_factor_file_correct:
        print("Factors file is not correct.")
    else:
        print("Factors file is loaded and checked")


def alternatives_file_info(file_checker):
    if not file_checker.is_alternatives_file_found:
        print("Alternatives file is not found")
    elif not file_checker.is_alternatives_file_correct:
        print("Alternatives file is not correct")
    else:
        print("Alternatives file is loaded and checked")


def factors_compare_file_info(file_checker):
    if not file_checker.is_factors_compare_file_found:
        print("Factors compare file is not found")
    elif not file_checker.is_factors_compare_file_correct:
        print("Factors compare file is not correct")
    else:
        print("Factors compare file is loaded and checked")


def alternatives_compares_file_info(file_checker):
    if not file_checker.is_alternatives_compares_file_found:
        print("Alternatives compares file is not found")
    elif not file_checker.is_alternatives_compares_file_correct:
        print("Alternatives compares file is not correct")
    else:
        print("Alternatives compares file is loaded and checked")


def interactive_input_info():
    print("You have to enter all values manually.")


def input_factors():
    print("You have to enter factors manually.")
    return __input_list("How many factors do you want to use? ", "Enter name of factor №")


def input_alternatives():
    print("You have to enter alternatives manually.")
    return __input_list("How many alternatives do you want to use? ", "Enter name of alternative №")


# 2DO: CR check
def input_factors_compare(relative_measurement):
    print("You have to enter factors compare matrix manually.")
    __print_rate_instruction()
    factors = relative_measurement.get_factors()
    for i in range(1, relative_measurement.get_factors_count() + 1):
        for j in range(1, relative_measurement.get_factors_count() + 1):
            if (j - i) > 0:
                question = 'Rate the importance of factor "%s" compared to factor "%s" [-8; 8] ' \
                           % (factors[i - 1], factors[j - 1])
                relative_measurement.set_factors_compare_matrix_element(i, j, __input_rate(question))


# 2DO: CR check
def input_alternatives_compares(relative_measurement):
    print("You have to enter alternatives compare matrixes manually.")
    __print_rate_instruction()
    factors = relative_measurement.get_factors()
    alternatives = relative_measurement.get_alternatives()
    for k in range(relative_measurement.get_factors_count()):
        print('Compare alternatives by factor "%s"' % factors[k])
        for i in range(1, relative_measurement.get_alternatives_count() + 1):
            for j in range(1, relative_measurement.get_alternatives_count() + 1):
                if (j - i) > 0:
                    question = 'Rate the alternative "%s" compared to the alternative "%s" [-8; 8] ' \
                               % (alternatives[i - 1], alternatives[j - 1])
                    relative_measurement.set_alternatives_compare_matrixes_element(k + 1, i, j, __input_rate(question))


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
            print('You must enter only positive integer number! Try again. \n')


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
            print('You must enter only integer number from -8 to 8! Try again. \n')


def __print_rate_instruction():
    insruction = ('Rating instruction:\n' +
                  'Rate\tDefenition\n' +
                  '0\t\tEqual preference\n' +
                  '1\t\tSmall preference\n' +
                  '2\t\tMedium Preference\n' +
                  '3\t\tAbove medium preference above medium\n' +
                  '4\t\tModerately strong preference\n' +
                  '5\t\tStrong preference\n' +
                  '6\t\tVery strong preference\n' +
                  '7\t\tVery, very strong preference\n' +
                  '8\t\tAbsolute preference\n' +
                  'Negative values [-8 -1] correspond to the inversion of the compared entities positions\n')
    print(insruction)
