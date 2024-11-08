from typing import TypeVar, Union

import pandas as pd
import numpy as np

DataFrame = TypeVar('pd.DataFrame')
column = TypeVar('pd.DataFrame.column')
array = TypeVar('np.array')

def markup(*independent_vars: Union[list[array], tuple[array]]) -> array:
    for array in independent_vars:
        sort_arr = np.sort(array)
        fir_quart = np.quantile(sort_arr, 0.25)
        sec_quart = np.quantile(sort_arr, 0.5)
        therd_quart = np.quantile(sort_arr, 0.75)

        sort_arr = np.reshape(sort_arr, (4, ))
    return sort_arr

def fuzzilation(target_var: array, *independent_vars: Union[list[array], tuple[array]]):
    pass
def calculate_tri_points():
    arr = np.reshape(np.arange(1, 13), 4, 3)
    return arr

def col_call(inp_list, arr):
    
    col_dict = {
        inp_list[0]: ['l', 'c', 'r'],
        inp_list[1]: arr[1],

        'abc': ['2']
    }
    return col_dict

def database():
    levels = np.array['low', 'medium', 'high']
    name_arr = np.array['bmi', 'schooling', 'income', 'life_exp']


    level_arr = np.array[levels, [levels[0], levels[2], levels[1]], [levels[2], levels[0], levels[1]], [levels[2], levels[1], levels[0]]]

    res_list = []
    for name in name_arr:
        level_
    for some in level_list:
        for level in some:
            tmp_list = []
            for name in name_list:
                tmp_list.append(name + ': ' + level)
            res_list.append(tmp_list.copy())
            tmp_list.clear()
    return res_list

def MUO(x: tuple, j, m):
    while j != m:
        pass

if __name__ == '__main__':
    x = ['zdfgdhjk', '2', '3']
    print(calculate_tri_points())