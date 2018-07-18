import csv
import os


def ensure_dir(path):
    """
    Create the folder if it's not exist
    @param path: Path including folder name
    @type path: string
    """
    directory = os.path.dirname(path)
    if not directory == '':
        if not os.path.exists(directory):
            os.makedirs(directory)


def glue_result(categories, weights, is_sort):
    """
    Assemble numbered list of categories with the corresponding list of weights
    @param categories: List of categories
    @type categories: list
    @param weights: List of weights
    @type weights: list
    @param is_sort: To sort members of result list by weights values
    @type is_sort: bool
    @return: Assembled list
    @rtype: list
    """
    result = []
    for i in range(len(categories)):
        result.append([i + 1, categories[i], weights[i]])
    if is_sort:
        result.sort(key=lambda lst: lst[2], reverse=True)
    return result


def round_vector(vector, digits_num):
    """
    Round values of the vector (column)
    @param vector: Column
    @type vector: list of floats
    @param digits_num: number of decimal places
    @type digits_num: int
    @return: Vector with rounded values
    @rtype: list
    """
    return [round(v, digits_num) for v in vector]


def round_matrix(matrix, digits_num):
    """
    Round values of the square matrix
    @param matrix: Column
    @type matrix: list[][]
    @param digits_num: number of decimal places
    @type digits_num: int
    @return: Matrix with rounded values
    @rtype: list[][]
    """
    result = matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            result[i, j] = round(matrix[i, j], digits_num)
    return result


def csv_to_list(file_path):
    """
    Import from csv-file to list
    @param file_path: Path to the csv file (including its name)
    @type file_path: string
    @return: Imported values
    @rtype: list
    """
    with open(file_path, newline='', encoding='utf-8') as file_obj:
        reader = csv.reader(file_obj)
        result = list(reader)
    return result


def list_to_csv(file_path, list_to_write):
    """
    Export from list to csv file
    @param file_path: Path to the csv file (including its name)
    @type file_path: string
    @param list_to_write: Values to export
    @type list_to_write: list
    """
    ensure_dir(file_path)
    with open(file_path, "w", newline='', encoding='utf-8') as file_obj:
        writer = csv.writer(file_obj, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        # print(list_to_write)
        for line in list_to_write:
            writer.writerow(line)


def str_list_to_float(processing_list):
    """
    Parser for list of strings which can include both float and '1/x'-like values
    @param processing_list: List for parse
    @type processing_list: list of strings
    @return: Parsed list
    @rtype: list of floats
    """
    for i in range(len(processing_list)):
        for j in range(len(processing_list[0])):
            split_list = processing_list[i][j].split('/')
            if len(split_list) == 1:
                processing_list[i][j] = float(split_list[0])
            else:  # x / y
                processing_list[i][j] = float(split_list[0]) / float(split_list[1])
    return processing_list


def get_fraction(float_value, round_digits_num):
    """
    Transform float value to '1/x'-like string. Integer values transformed to its common string representation
    @param float_value: Value for transform
    @type float_value: float
    @param round_digits_num: Number of decimal places for round
    @type round_digits_num: int
    @return: Result of tranformation
    @rtype: string
    """
    float_to_fraction = {
        round(1 / 2, round_digits_num): '1/2',
        round(1 / 3, round_digits_num): '1/3',
        round(1 / 4, round_digits_num): '1/4',
        round(1 / 5, round_digits_num): '1/5',
        round(1 / 6, round_digits_num): '1/6',
        round(1 / 7, round_digits_num): '1/7',
        round(1 / 8, round_digits_num): '1/8',
        round(1 / 9, round_digits_num): '1/9'
    }
    float_value = round(float_value, round_digits_num)
    if 0 < float_value < 1:
        return float_to_fraction[float_value]
    else:
        return str(int(float_value))


if __name__ == '__main__':
    print('This module is intended only for import, not for execution!')
