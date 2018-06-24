
def glue_result(categories, weights, is_sort):
    result = []
    for i in range(len(categories)):
        result.append([i + 1, categories[i], weights[i]])
    if is_sort:
        result.sort(key=lambda lst: lst[2], reverse=True)
    return result


def round_vector(vector, digits_num):
    return [round(v, digits_num) for v in vector]


def round_matrix(matrix, digits_num):
    result = matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            result[i, j] = round(matrix[i, j], digits_num)
    return result
