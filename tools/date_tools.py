# -*- coding: utf-8 -*-

"""
    封装处理处理时间相关方法
"""

import datetime
import logging
import calendar
import time
_logger = logging.getLogger(__name__)


def time_cost(f):
    """
    :param f: function
    :return: 计算函数耗时多久
    """
    def _wrapper(*args, **kwargs):
        now = time.time()
        res = f(*args, **kwargs)
        log_txt = u'函数 %s 耗时 %.2fs!' % (f.__name__, time.time() - now)
        _logger.info(log_txt)
        print(log_txt)
        return res
    return _wrapper


def date_range(begin_date, end_date):
    """
        获取一个时间区间的list
    """
    dates = []
    dt = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    date = begin_date[:]
    while date <= end_date:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates


def get_month_begin_and_end(date_str=False):
    """
        获取某个月的月初和月末
        date_str: '2012-12-12' 默认是当天
    """
    if date_str:
        today = time.strptime(date_str[:10], '%Y-%m-%d')
    else:
        today = time.localtime()
    # 月初肯定是1号
    day_begin = '%d-%02d-01' % (today.tm_year, today.tm_mon)
    # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
    wday, month_range = calendar.monthrange(today.tm_year, today.tm_mon)
    day_end = '%d-%02d-%02d' % (today.tm_year, today.tm_mon, month_range)
    return day_begin, day_end


def add_months(dt, months):
    """
        月加减
    """
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def get_week_of_month(year, month, day):
    """
    获取指定的某天是某个月中的第几周
    周一作为一周的开始
    """
    end = int(datetime.datetime(year, month, day).strftime("%W"))
    begin = int(datetime.datetime(year, month, 1).strftime("%W"))
    return end - begin + 1


def check_year_month(year_month):
    """
        年月的格式判断
            e.g. 2018-12
    """
    year_month = str(year_month)
    try:
        datetime.datetime.strptime(year_month + '-01', '%Y-%m-%d')
        return True
    except:
        return False


def add_hours(date_str, hours=8):
    """
    :param date_str: `2018-11-07 15:16:33`
    :param hours: int
    :return: string: `2018-11-07 23:16:33`
    """
    if not date_str:
        return date_str
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    dt = dt + datetime.timedelta(hours=hours)
    return dt.strftime("%Y-%m-%d %H:%M:%S")
