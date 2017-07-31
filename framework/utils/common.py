# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2016/11/29 14:52
"""
import json
import random
import hashlib
import uuid
import sys

import datetime
from calendar import EPOCH

import math
from pip.compat import total_seconds

reload(sys)
sys.setdefaultencoding('utf-8')

__ALPHA = "abcdefghijklmnopqrstuvwxyz"
__CHARS = __ALPHA + __ALPHA.upper() + "!@#$%^&*()"


def generate_password(n=12):
    """
    生成指定位数的随机密码
    :param n: 位数 默认12
    :return: 密码字符串
    """
    index = random.sample(range(0, len(__CHARS)), n)
    return reduce(lambda a, b: a + b, [__CHARS[x] for x in index])


def build_ret(success, msg="", total=0, data=[], code=0):
    """
    生成请求响应json
    :param success: type(boolean) 成功或失败
    :param msg: type(str) 额外信息
    :param total: type(int) 数据总数(用于分页)
    :param data: type(list) 数据
    :param code: type(int) 错误代号
    :return: format of json is:
    {
      "data": []
      "total": 0,
      "msg": "",
      "code": 0
    }
    """

    def tran_code(flag):
        if flag:
            return 0
        else:
            return 1

    if code == 0:
        code = tran_code(success)

    dic = {
        "code": code,
        "msg": msg,
        "total": total,
        "data": data
    }
    return json.dumps(dic, ensure_ascii=False)


def get_ret(error, total=0, msg=None, *data):
    """
    生成请求响应json
    :param total: type(int) 数据总数(用于分页)
    :param data: type(list) 数据
    :param error: type(error) 错误类
    :param msg: type(str) 额外信息
    :return: format of json is:
    {
      "code": 0,
      "data": []
      "total": 0,
      "msg": ""
    }
    """
    if msg is None:
        msg = error.msg
    dic = {
        "code": error.code,
        "msg": msg,
        "total": total,
        "data": data
    }
    return json.dumps(dic, ensure_ascii=False)


def md5(str):
    """
    生成MD5值
    :param str:
    :return:
    """
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def get_uuid():
    """
    由MAC地址、当前时间戳、随机数生成(83be7c1e152d11e78f8cd8cb8aca49be)
    :return: type(String)
    """
    return str(uuid.uuid1()).replace('-', '')


def timestamp_now():
    return datetime2timestamp(datetime.datetime.now())


def datetime2timestamp(dt, convert_to_utc=False):
    """ Converts a datetime object to UNIX timestamp in milliseconds. """
    if isinstance(dt, datetime.datetime):
        if convert_to_utc:  # 是否转化为UTC时间
            dt = dt + datetime.timedelta(hours=-8)  # 中国默认时区
        timestamp = total_seconds(dt - EPOCH)
        return long(timestamp)
    return dt


def date_time(day_offset=0, seconds_offset=0, microseconds_offset=0, milliseconds_offset=0, minutes_offset=0,
              hours_offset=0, weeks_offset=0, fmt="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间
    :param day_offset:
    :param seconds_offset:
    :param microseconds_offset:
    :param milliseconds_offset:
    :param minutes_offset:
    :param hours_offset:
    :param weeks_offset:
    :param fmt: 格式化字符串
    :return:
    """
    _date_time = datetime.datetime.now() + datetime.timedelta(days=day_offset,
                                                              seconds=seconds_offset,
                                                              microseconds=microseconds_offset,
                                                              milliseconds=milliseconds_offset,
                                                              minutes=minutes_offset,
                                                              hours=hours_offset,
                                                              weeks=weeks_offset)
    return _date_time.strftime(fmt)


def retry_func(count, interval, func, *args, **kwargs):
    """
    方法重试
    :param count: 重试次数
    :param interval: 间隔(s)
    :param func: 待重试的方法，执行失败，需要抛出异常，否则默认执行成功不继续重试
    :param args:
    :param kwargs:
    :return:
    """
    from time import sleep
    while count > 0:
        try:
            return func(*args, **kwargs)
        except Exception, e:
            count -= 1
            if count == 0:
                raise e
            sleep(interval)


def byte_format(size, unit='bytes'):
    units = ['bytes', 'K', 'M', 'G', 'T', 'P']
    return float(size) / math.pow(1024, units.index(unit))


def to_byte(size, unit='bytes'):
    units = ['bytes', 'K', 'M', 'G', 'T', 'P']
    return float(size) * math.pow(1024, units.index(unit))
