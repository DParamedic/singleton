from typing import TypeVar, Union

import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

DataFrame = TypeVar('pd.DataFrame')
column = TypeVar('pd.df.column')
array = TypeVar('np.array')
rules = TypeVar('fuzz.ctrl.Rule')

def mu_value(independent_var: int, sort_arr: array, term_value: tuple) -> tuple[int]:
    """
    #Параметры:
    independent_var -- значение переменной, для которой необходимо найти значение функции
    sort_arr -- массив, на котором определена переменная
    term_value -- термы.
    #Вывод:
    На выходе функции кортеж из чисел, которые отображают значение функции для каждого терма.
    """
    return tuple(fuzz.interp_membership(sort_arr, term_value[i], independent_var) for i in range(len(term_value)))

def body_func(data_frame: DataFrame, target_var: str, *independent_vars: str, print_pyplot: bool=False) -> array:
    """
    У входных данных (независимых переменных) ограничение по количеству, оно должно равняться трем, иначе генерируется ошибка.
    Причина генерации ошибки -- формирование базы данных.
    """
    if len(independent_vars) != 3:
        raise ValueError('Необходимо три нецелевых параметра для *independent_vars.')
    (name_list := [i for i in independent_vars]).append(target_var)
    statistic_dict = {}
    arr_sort_dict = {}
    term_build_dict = {}
    ruls_base = {}
    range_dict = {}
    for name in name_list:
        statistic_dict[name] = (data_frame[name].min(), data_frame[name].mean(), data_frame[name].max())
    for name in name_list:
        arr_sort_dict[name] = np.sort(np.array(data_frame[name].tolist()))
    # Определение треугольных функций принадлежности
    for name in name_list:
        term_build_dict[name] = (
            fuzz.trimf(arr_sort_dict[name], [statistic_dict[name][0], statistic_dict[name][0], statistic_dict[name][1]]),
            fuzz.trimf(arr_sort_dict[name], [statistic_dict[name][0], statistic_dict[name][1], statistic_dict[name][2]]),
            fuzz.trimf(arr_sort_dict[name], [statistic_dict[name][1], statistic_dict[name][2], statistic_dict[name][2]])
        )
    # Визуализация функций принадлежности
    if print_pyplot: # Можно вставить условие визуализации
        fig, axes = plt.subplots(1, 4, figsize=(24, 5))
        for name in name_list:
            axes[name_list.index(name)].plot(arr_sort_dict[name], term_build_dict[name][0], label='Low', color='blue')
            axes[name_list.index(name)].plot(arr_sort_dict[name], term_build_dict[name][1], label='Medium', color='green')
            axes[name_list.index(name)].plot(arr_sort_dict[name], term_build_dict[name][2], label='High', color='red')
            axes[name_list.index(name)].set_title(f'{name} Membership Function')
            axes[name_list.index(name)].set_xlabel(f'{name}')
            axes[name_list.index(name)].set_ylabel('%')
            axes[name_list.index(name)].legend()
        plt.tight_layout()
        plt.show()
        return
    
    # База правил
    # Узкое горлышко, потому что работает только с тремя входящеми переменными. По хорошему надо переписать.
    
    # Определение диапазонов на основе фактических данных
    # Не понимаю, как работает
    # for name in name_list[0:3]:
    #     range_dict[name] = ctrl.Antecedent(np.linspace(statistic_dict[name][0], statistic_dict[name][2], 100), name)
    # range_dict[name_list[-1]] = ctrl.Consequent((statistic_dict[name_list[-1]][0], statistic_dict[name_list[-1]][2] + 0.1, 0.1), name_list[-1])

    for name in name_list:
        ruls_base[name] = 'low', 'medium', 'high'

    # for var, terms in zip(variables, intervals_data.values()): # [(range_dict[name], ruls_base[name]), ...]
    #     intervals = np.linspace(var.universe.min(), var.universe.max(), num_intervals + 1)
    #     for term, (start, end) in zip(terms, zip(intervals, intervals[1:])):
    #         var[term] = fuzz.trimf(var.universe, [start, (start + end) / 2, end])

    def rec_ruls(ruls_base: dict, name_list: list) -> tuple[array, rules]:
        if len(name_list) == 1:
            rule = ctrl.Rule(
                range_dict[name_list[0]][x1] & range_dict[name_list[1]][x2] & range_dict[name_list[2]][x3],
                range_dict[name_list[-1]][y]
            )
    rules = []
    for x1 in ruls_base[name_list[0]]:
        for x2 in ruls_base[name_list[1]]:
            for x3 in ruls_base[name_list[2]]:
                for y in ruls_base[name_list[-1]]:
                    rule = ctrl.Rule(
                        range_dict[name_list[0]][x1] & range_dict[name_list[1]][x2] & range_dict[name_list[2]][x3],
                        range_dict[name_list[-1]][y]
                    )
                    rules.append(rule)
