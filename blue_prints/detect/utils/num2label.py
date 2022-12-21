# -*- coding: utf-8 -*-
"""
@author: zhangshihao
@file: num2label.py
@time: 2022/12/16 12:26
"""

"""
    if label == '尿酸结晶':
        label = "UricAcid"
    elif label == "一水草酸钙结晶":
        label = "CalciumOxalateMonohydrate"
    elif label == "二水草酸钙结晶":
        label = "CalciumOxalateDihydrate"
    elif label == "磷酸铵镁结晶":
        label = "MagnesiumAmmoniumPhosphate"
    elif label == "磷酸钙结晶":
        label = "CalciumPhosphate"
    elif label == "胱氨酸结晶":
        label = "Cystine"
    elif label == "不定型尿酸":
        label = "AmorphousUricAcid"
    elif label == "不定型磷酸钙":
        label = "UnshapedCalciumPhosphate"
    elif label == "尿酸氨":
        label = "Uridine"
    elif label == "尿酸钠":
        label = "SodiumUrate"
    else:
        label = "None"
"""


def num2label(num):
    if num == 0:
        label = "一水草酸钙结晶"
    elif num == 1:
        label = "二水草酸钙结晶"
    elif num == 2:
        label = "碳酸钙"
    elif num == 3:
        label = "磷酸钙结晶"
    elif num == 4:
        label = "尿酸结晶"
    elif num == 5:
        label = "磷酸铵镁结晶"
    elif num == 6:
        label = "胱氨酸结晶"
    elif num == 7:
        label = "尿酸氨"
    elif num == 8:
        label = "不定型磷酸钙"
    elif num == 9:
        label = "不定型尿酸"
    return label
