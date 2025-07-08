#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
from datetime import datetime, timedelta


def getDateTime():
    '''
    获取当前日期时间，格式'20150708085159'
    '''
    return time.strftime(r'%Y%m%d%H%M%S', time.localtime(time.time()))


def timestamp():
    """
    时间戳
    """
    return time.time()


def timestamp13():
    """
    13位时间戳
    """
    return "%d%s" % (int(datetime.now().timestamp()),
                     str(datetime.now().microsecond))


def datetime_strftime(fmt="%Y%m"):
    """
    格式化datetime时间
    :param fmt "%Y%m%d%H%M%S"
    """
    return datetime.now().strftime(fmt)

def current_time(fmt="%Y-%m-%d %H:%M:%S"):
    """
    格式化datetime时间
    :param fmt "%Y%m%d%H%M%S"
    """
    return datetime.now().strftime(fmt)

def future_time(minute):
    # 获取当前时间
    now = datetime.now()

    # 计算2分钟后的时间
    one_minutes_later = now + timedelta(minutes=minute)

    return one_minutes_later.strftime("%Y-%m-%d %H:%M:%S")


def time_sleep(t):
    """
    等待时间
    :param t
    """
    return time.sleep(t)


if __name__ == "__main__":
    # a = '"result":"success"'
    # b = '{"result":"success"}'
    # print(a in b)
    # print(time_sleep(3))
    print(datetime_strftime('%Y%m%d'))