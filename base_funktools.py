from typing import TypeVar, Union

import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

DataFrame = TypeVar('pd.DataFrame')
column = TypeVar('pd.df.column')
arrayLike = TypeVar('np.array')
rules = TypeVar('fuzz.ctrl.Rule')

def mu_value(independent_var: int, sort_arr: arrayLike, term_value: tuple) -> tuple[int]:
    """
    #Параметры:
    independent_var -- значение переменной, для которой необходимо найти значение функции
    sort_arr -- массив, на котором определена переменная
    term_value -- термы.
    #Вывод:
    На выходе функции кортеж из чисел, которые отображают значение функции для каждого терма.
    """
    return tuple(fuzz.interp_membership(sort_arr, term_value[i], independent_var) for i in range(len(term_value)))

def ruls_base(variables_list: list, term_arr, target_term_arr=None) -> arrayLike:
    '''
    #Параметры:
    variables_list -- список переменных.
    term_arr -- список терм.
    target_term_arr -- список альтернативных значений для терм(например, для синглтона).

    '''
    stop_word: int = len(term_arr)**len(variables_list)
    def rec(term_arr, stop_word: int, target_term_arr, res_arr=None):
        len_term_arr = len(term_arr)
        shape_res_arr = np.shape(res_arr)
        if res_arr is None:
            res_arr = np.array(np.array([
                np.repeat(np.array([i for i in term_arr]), len_term_arr),
                [i for i in term_arr]*len_term_arr
                ]))
            return rec(term_arr, stop_word, target_term_arr, res_arr)
        elif shape_res_arr[1] == stop_word:
            return res_arr
        elif shape_res_arr[1]*len_term_arr == stop_word:
            if target_term_arr is not None and len(target_term_arr) == len_term_arr:
                term_arr = target_term_arr
                res_arr = np.reshape(np.repeat(res_arr, len_term_arr), (shape_res_arr[0], shape_res_arr[1]*len_term_arr))
                res_arr = np.reshape(np.append(res_arr, [i for i in term_arr]*len_term_arr**shape_res_arr[0]), (shape_res_arr[0]+1, shape_res_arr[1]*len_term_arr))
                return rec(term_arr, stop_word, target_term_arr, res_arr)
        else:
            res_arr = np.reshape(np.repeat(res_arr, len_term_arr), (shape_res_arr[0], shape_res_arr[1]*len_term_arr))
            res_arr = np.reshape(np.append(res_arr, [i for i in term_arr]*len_term_arr**shape_res_arr[0]), (shape_res_arr[0]+1, shape_res_arr[1]*len_term_arr))
            return rec(term_arr, stop_word, target_term_arr, res_arr)
    return np.transpose(rec(term_arr, stop_word, target_term_arr))

def body_func(data_frame: DataFrame, target_var: str, *independent_vars: str, print_pyplot: bool=False) -> arrayLike:
    """

    """
    (name_list := [i for i in independent_vars]).append(target_var)
    statistic_dict = {}
    arr_sort_dict = {}
    term_build_dict = {}
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
    if print_pyplot: 
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
    
    term_list = ['low', 'medium', 'high']
    base_ruls = ruls_base(name_list, term_list, [statistic_dict[target_var][0], statistic_dict[target_var][1], statistic_dict[target_var][2]])
    