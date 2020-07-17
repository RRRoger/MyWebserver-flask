# coding=utf-8

from random import Random


def random_str(length=10):
    res = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    char_length = len(chars) - 1
    random = Random()
    for i in range(length):
        res += chars[random.randint(0, char_length)]
    return res


def int_length(num):
    """
    计算一个整数是几位数
    :param num:
    :return:
    """
    cnt = 0
    num = abs(num)
    while num:
        num //= 10
        cnt += 1
    return cnt
