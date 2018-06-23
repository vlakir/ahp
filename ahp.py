import numpy as np
import maimodules.matclasses as mc


alternatives = ['Дом 1', 'Дом 2', 'Дом 3']

factors = ['Размер', 'Транспорт', 'Окружение', 'Возраст', 'Двор', 'Удобства', 'Состояние', 'Финансы']

alternatives_count = len(alternatives)
factors_count = len(factors)

factors_compare_array = np.mat([[1, 5, 3, 7, 6, 6, 1 / 3, 1 / 4],
                                [1/5, 1, 1/3, 5, 3, 3, 1/5, 1/7],
                                [1/3, 3, 1, 6, 3, 4, 1/2, 1/5],
                                [1/7, 1/5, 1/6, 1, 1/3, 1/4, 1/7, 1/8],
                                [1/6, 1/3, 1/3, 3, 1, 1/2, 1/5, 1/6],
                                [1/6, 1/3, 1/4, 4, 2, 1, 1/5, 1/6],
                                [3, 5, 2, 7, 5, 5, 1, 1/2],
                                [4, 7, 5, 8, 6, 6, 2, 1]])

ahp_container = mc.AhpContainer(alternatives, factors)
ahp_container.set_factors_compare_matrix_elements(factors_compare_array)

alternatives_compare_array = np.mat([[1, 5, 9],
                                     [1/5, 1, 4],
                                     [1/9, 1/4, 1]])
ahp_container.set_alternatives_compare_matrixes_elements(1, alternatives_compare_array)

alternatives_compare_array = np.mat([[1, 4, 1 / 5],
                                     [1/4, 1, 1/9],
                                     [5, 9, 1]])
ahp_container.set_alternatives_compare_matrixes_elements(2, alternatives_compare_array)

alternatives_compare_array = np.mat([[1, 9, 4],
                                     [1/9, 1, 1/4],
                                     [1/4, 4, 1]])
ahp_container.set_alternatives_compare_matrixes_elements(3, alternatives_compare_array)

alternatives_compare_array = np.mat([[1, 1, 1],
                                     [1, 1, 1],
                                     [1, 1, 1]])
ahp_container.set_alternatives_compare_matrixes_elements(4, alternatives_compare_array)

alternatives_compare_array = np.mat([[1, 6, 4],
                                     [1/6, 1, 1/3],
                                     [1/4, 3, 1]])
ahp_container.set_alternatives_compare_matrixes_elements(5, alternatives_compare_array)

alternatives_compare_array = np.mat([[1, 9, 6],
                                     [1/9, 1, 1/3],
                                     [1/6, 3, 1]])
ahp_container.set_alternatives_compare_matrixes_elements(6, alternatives_compare_array)

alternatives_compare_array = np.mat([[1, 1 / 2, 1 / 2],
                                     [2, 1, 1],
                                     [2, 1, 1]])
ahp_container.set_alternatives_compare_matrixes_elements(7, alternatives_compare_array)

alternatives_compare_array = np.mat([[1, 1 / 7, 1 / 5],
                                     [7, 1, 3],
                                     [5, 1/3, 1]])
ahp_container.set_alternatives_compare_matrixes_elements(8, alternatives_compare_array)

ahp_container.calculate()

print(ahp_container.to_string())
