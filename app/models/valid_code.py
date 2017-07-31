#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/1 14:21
"""
import random
import uuid
import json
from app.conf.config import web, red_pre,R_SMS
from framework.db import db
from framework.utils.common import get_uuid, date_time
from app.conf import msg
from app.untils.sms import send_sms_dy as send


r = db['redis']


def generate_code():
    """
    生成6位短信验证码
    :return: 
    """
    random_seeds = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    str_slice = random.sample(random_seeds, 6)
    sms_code = ''.join(str_slice)
    return sms_code


def _generate_uuid():
    """
    生成一个字符串序号，用于标识一次短信验证码推送
    :return: 
    """
    business_id = uuid.uuid1()
    return business_id


def set_code(sms_code, mobile):
    """
    存储短信验证码，生命周期为60s
    :param sms_code: type(string) 短信验证码
    :param mobile:  type(string) 手机号
    :return: 
    """
    r.setex(mobile+red_pre['code'], R_SMS['redis_timeout'], sms_code)
    pass


def get_code(mobile):
    """
    从redis取出短信验证码
    :param mobile: type(string) 手机号
    :return: 
    """
    return r.get(mobile)


def send_sms(mobile):
    """
    处理短语验证码发送的逻辑函数
    :param mobile: type(string) 手机号
    :return: 
    """
    if get_code(mobile+red_pre['code']):
        return msg.A_MAX_REQUEST
    __param = {}
    __sms_code = generate_code()
    __uuid = _generate_uuid()
    __param[R_SMS['template_string']] = __sms_code
    param = json.dumps(__param)
    sms_response = send(__uuid, mobile,param)
    if sms_response:
        set_code(__sms_code, mobile)
        return msg.SUCCESS
    else:
        return msg.A_SMS_ERR


def add_code_redis(uuid_str, code):
    """
    存储验证码到redis
    :param uuid_str:
    :param code:
    :return:
    """
    r.set(red_pre['captcha'] + uuid_str, code, ex=60)


def get_captcha(uuid_str):
    """
    获取验证码并删除
    :param uuid_str:
    :return:
    """
    c = red_pre['captcha'] + uuid_str
    return __get_key__(c)


def __get_key__(code, is_del=True):
    """
    获取key,删除并返回value
    :param code:
    :return:
    """
    val = r.get(code)
    if is_del:
        va = r.delete(code)
        print va
    return val

if __name__ == '__main__':
    # a = send_sms('13247780947')
    # print  r.setex('test', 60, "123")
    # print r.get('test')
    # print r.get('test')
    pass

    # print r.get('test')
    # print r.get('test')

    # params = "{\"smscode\":\"12345\"}"
    # print type(params), params
