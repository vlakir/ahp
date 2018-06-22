import numpy as np
import maimodules.matclasses as mc


alternatives = ['Дом 1', 'Дом 2', 'Дом 3']

factors = ['Размер', 'Транспорт', 'Окружение', 'Возраст', 'Двор', 'Удобства', 'Состояние', 'Финансы']

alternatives_count = len(alternatives)
factors_count = len(factors)

factors_compare_matrix = np.mat([[1, 5, 3, 7, 6, 6, 1/3, 1/4],
                                [1/5, 1, 1/3, 5, 3, 3, 1/5, 1/7],
                                [1/3, 3, 1, 6, 3, 4, 1/2, 1/5],
                                [1/7, 1/5, 1/6, 1, 1/3, 1/4, 1/7, 1/8],
                                [1/6, 1/3, 1/3, 3, 1, 1/2, 1/5, 1/6],
                                [1/6, 1/3, 1/4, 4, 2, 1, 1/5, 1/6],
                                [3, 5, 2, 7, 5, 5, 1, 1/2],
                                [4, 7, 5, 8, 6, 6, 2, 1]])

factors_matrix = mc.CompareMatrix(factors_count)
factors_matrix.set_categories(factors)
factors_matrix.set_matrix(factors_compare_matrix)
factors_matrix.calculate()

# noinspection PyUnresolvedReferences
alternatives_compare_matrix = ([np.zeros(shape=(alternatives_count, alternatives_count)) for i in range(factors_count)])

compare_matrix = np.mat([[1, 5, 9],
                        [1/5, 1, 4],
                        [1/9, 1/4, 1]])
alternatives_compare_matrix[0] = mc.CompareMatrix(alternatives_count)
alternatives_compare_matrix[0].set_matrix(compare_matrix)
alternatives_compare_matrix[0].set_categories(alternatives)

compare_matrix = np.mat([[1, 4, 1/5],
                        [1/4, 1, 1/9],
                        [5, 9, 1]])
alternatives_compare_matrix[1] = mc.CompareMatrix(alternatives_count)
alternatives_compare_matrix[1].set_matrix(compare_matrix)
alternatives_compare_matrix[1].set_categories(alternatives)

compare_matrix = np.mat([[1, 9, 4],
                        [1/9, 1, 1/4],
                        [1/4, 4, 1]])
alternatives_compare_matrix[2] = mc.CompareMatrix(alternatives_count)
alternatives_compare_matrix[2].set_matrix(compare_matrix)
alternatives_compare_matrix[2].set_categories(alternatives)

compare_matrix = np.mat([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]])
alternatives_compare_matrix[3] = mc.CompareMatrix(alternatives_count)
alternatives_compare_matrix[3].set_matrix(compare_matrix)
alternatives_compare_matrix[3].set_categories(alternatives)

compare_matrix = np.mat([[1, 6, 4],
                        [1/6, 1, 1/3],
                        [1/4, 3, 1]])
alternatives_compare_matrix[4] = mc.CompareMatrix(alternatives_count)
alternatives_compare_matrix[4].set_matrix(compare_matrix)
alternatives_compare_matrix[4].set_categories(alternatives)

compare_matrix = np.mat([[1, 9, 6],
                        [1/9, 1, 1/3],
                        [1/6, 3, 1]])
alternatives_compare_matrix[5] = mc.CompareMatrix(alternatives_count)
alternatives_compare_matrix[5].set_matrix(compare_matrix)
alternatives_compare_matrix[5].set_categories(alternatives)

compare_matrix = np.mat([[1, 1/2, 1/2],
                        [2, 1, 1],
                        [2, 1, 1]])
alternatives_compare_matrix[6] = mc.CompareMatrix(alternatives_count)
alternatives_compare_matrix[6].set_matrix(compare_matrix)
alternatives_compare_matrix[6].set_categories(alternatives)

compare_matrix = np.mat([[1, 1/7, 1/5],
                        [7, 1, 3],
                        [5, 1/3, 1]])
alternatives_compare_matrix[7] = mc.CompareMatrix(alternatives_count)
alternatives_compare_matrix[7].set_matrix(compare_matrix)
alternatives_compare_matrix[7].set_categories(alternatives)

indx = 1
alternatives_compare_matrix[indx].calculate()
print(alternatives_compare_matrix[indx].to_string())

