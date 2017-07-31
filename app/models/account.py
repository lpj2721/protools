#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/6/30 11:33
"""
from app.conf.config import web, red_pre
from app.conf import msg
from framework.db import db, mongo_command
from framework.utils.common import get_uuid, date_time
from jot import jwt, jws
import time, string,random

collection = db['mongodb']
r = db['redis']

# 个人用户注册


def person_register(params):
    """
    :param params: type(list(dict))
    :return:
    """
    pwd = params['pwd']
    re_pwd = params['re_pwd']
    sms_code = params['code']
    mobile = params['mobile']
    check_result = verify_code(mobile,sms_code)
    if check_result is None:
        return msg.A_CODE_TIMEOUT
    elif check_result:
        if pwd == re_pwd:
            status = 2
            username = mobile + "-g"
            info_id = person_info_register(pwd, mobile)
            login_info = [
                (mobile, status, info_id),
                (username, status, info_id)
            ]
            login_info_register(login_info)
            return msg.SUCCESS
        else:
            return msg.A_PWD_ERR
    return msg.A_CODE_ERR

    # data['_id'] = get_uuid()
    # data['create_time'] = date_time()
    # data['status'] = 2
    # collection.insert_one(data)


def person_info_register(password, mobile):
    """
    注册个人信息表
    :param password: type(string) 密码
    :param mobile:  type(string) 手机号
    :return: _id
    """
    nickname = mobile + "_g"
    create_time = date_time()
    info_data = {
        'nickname': nickname,
        'username': nickname,
        'mobile': mobile,
        'password': password,
        'head_pic': "",
        'create_time': create_time
    }
    info_id = collection['UserInfo'].insert_one(info_data).inserted_id
    return info_id


def login_info_register(*login_info):
    """
    注册登录信息表
    :param login_info: type(list) 登录信息 eg:[("username1","type",info_id),("username2","type",info_id)]
    :return: 
    """
    print login_info
    for each in login_info[0]:
        each_info = dict()
        each_info['_id'], each_info['status'], each_info['info_id'] = each
        print each_info
        collection['UserLoginInfo'].insert_one(each_info)


def verify_code(mobile, sms_code):
    """
    短信验证码核对
    :param mobile: 
    :param sms_code: 
    :return: 
    """
    redis_code = r.get(mobile+red_pre['code'])
    if redis_code:
        if redis_code == sms_code:
            return True
        else:
            return False
    else:
        return None
        # return True


# 登陆功能


def person_login(username, pwd):
    """
    登陆的逻辑处理程序，返回一个token
    :param username: 
    :param pwd: 
    :return: 
    """
    if is_exists({'_id': username}):
        if valid_pwd(username,pwd):
            return msg.SUCCESS
        else:
            return msg

    pass


def generate_token(username):
    iat = time.time()
    exp = iat + web['session_timeout']
    payload = {
        'username': username,
        'iat': iat,
        'exp': exp
    }
    key_pix = token_key()
    token = jwt.encode(payload,signer=jws.HmacSha(bits=256, key=web['token_key']+key_pix))
    r.set(token, key_pix)
    return token


def token_key():
    """
    生成秘钥字符串
    :return: 
    """
    base_str = string.digits + string.letters
    key_list = [random.choice(base_str) for i in range(web['key_len'])]
    key_str = "".join(key_list)
    return key_str


def valid_pwd(index_id, pwd):
    """
    核对密码是否正确
    :param index_id: 索引id,用于查找用户信息表 
    :param pwd: 待核对的密码
    :return: 
    """

    source_pwd = collection['UserInfo'].find_one(index_id, {'_id': 0, 'password':  1})
    if pwd == source_pwd['password']:
        return True
    else:
        return False


# 注销功能
def delete_token_key(token):
    """
    删除redis中token-> key_pix映射
    :param token: 
    :return: 
    """
    r.delete(token)
    return True


# 企业注册
def company_register(params):
    """
    :param params: type(list(dict))
    :return:
    """
    pwd = params['pwd']
    re_pwd = params['re_pwd']
    username = params['username']
    mobile = params['mobile']
    if pwd == re_pwd:
        status = 1
        info_id = person_info_company(pwd, mobile, username)
        login_info = [
            (mobile, status, info_id),
            (username, status, info_id)
        ]
        login_info_company(login_info)
        return msg.SUCCESS
    else:
        return msg.A_PWD_ERR


def login_info_company(*login_info):
    """
    注册登录信息表
    :param login_info: type(list) 登录信息 eg:[("username1","type",info_id),("username2","type",info_id)]
    :return: 
    """
    print login_info
    for each in login_info[0]:
        each_info = dict()
        each_info['_id'], each_info['status'], each_info['info_id'] = each
        collection['UserLoginInfo'].insert_one(each_info)


def person_info_company(password, mobile, username):
    """
    注册企业信息表
    :param password: type(string) 密码
    :param mobile:  type(string) 手机号
    :param username:  type(string) 手机号
    :return: _id
    """
    nickname = mobile + "_g"
    create_time = date_time()
    company_id = get_uuid()
    company_info = {
        "_id": company_id,
        "create_time": create_time,
        "host": username,
        "name": "",
        "logo": "",
        "province": "",
        "company_type": "",
        "company_address": "",
        "address": "",
        "tele_person": "",
        "telephone": "",
        "fix_phone": "",
        "website": "",
        "description": "",
        "page_urls": [],
        "product": [],
        "fax": "1356343",
        "organization_code": "",
        "certificate": "",
        "production_license": "",
        "checkout": ""
    }
    collection['CompanyInfo'].insert_one(company_info)
    user_id = get_uuid()
    info_data = {
        '_id': user_id,
        'nickname': nickname,
        'username': username,
        'mobile': mobile,
        'password': password,
        'head_pic': "",
        'create_time': create_time,
        'company': company_id
    }
    collection['UserInfo'].insert_one(info_data)
    return user_id



def del_user_redis(ssid, e_name, pp_name):
    """
    删除ssid
    :param ssid:
    :param e_name:
    :param pp_name:
    :return:
    """
    r.delete(red_pre['ssid_acc'] + ssid)
    r.hdel(e_name, pp_name)


def add_code_redis(captcha_uuid, code):
    """
    存储验证码到redis
    :param captcha_uuid:
    :param code:
    :return:
    """
    r.set(red_pre['captcha'] + captcha_uuid, code, ex=60)


def is_exists(cond):
    """
    :param cond: type(dict) 查询条件
    :param projection: type(dict) 指定查询的字段(0,false-->不显示; 1,true-->显示)
    :return:node
    """
    result = collection['UserLoginInfo'].find_one(cond)
    if result is None:
        return False
    return result


def add_user_err(username, offset=1):
    """
    用户登录时输入错误后添加错误次数
    :param username: type(string) 账号
    :param offset: type(int) 偏移步长
    :return:
    """
    counts = get_user_err(username)
    counts += offset
    r.set(red_pre['acc_login_err'] + username, counts, web['account_freeze_time'])
    return counts


def get_user_err(username):
    """
    获取用户登录时输入错误次数
    :param username: type(string) 账号
    :return:
    """
    counts = r.get(red_pre['acc_login_err'] + username)
    if counts is None:
        counts = 0
    else:
        counts = int(counts)
    return counts


def del_user_err(username):
    """
    用户登录成功后删除输入错误后添加错误次数
    :param username: type(string) 账号
    :return:
    """
    return r.delete(red_pre['acc_login_err'] + username)


def get_captcha(uuid):
    """
    获取验证码并删除
    :param uuid:
    :return:
    """
    c = red_pre['captcha'] + uuid
    return __get_key__(c)