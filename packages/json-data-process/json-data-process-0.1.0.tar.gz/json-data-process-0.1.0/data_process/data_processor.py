# coding:utf-8
"""批量处理一些数据，如去空格、保留两位小数等"""


def trim_string(value):
    if isinstance(value, str):
        return value.strip()
    return value


def trim_dict(d):
    return {key: trim_value(value) for key, value in d.items()}


def trim_list(lst):
    return [trim_value(item) for item in lst]


def trim_value(value):
    """去除字符串两边空格"""
    if isinstance(value, str):
        return trim_string(value)
    elif isinstance(value, dict):
        return trim_dict(value)
    elif isinstance(value, list):
        return trim_list(value)
    else:
        return value


def round_floats(data, digits: int = 2):
    """
    float保留两位小数
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, float):
                data[key] = round(value, digits)
            elif isinstance(value, (list, dict)):
                round_floats(value)
    elif isinstance(data, list):
        for item in data:
            round_floats(item)
    return data
