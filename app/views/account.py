#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/6/30 11:16
"""

from flask import request, make_response
from framework.utils import sendmail
from app.conf.config import web
from app.models import account
from framework.utils.common import get_ret,build_ret
from framework.utils.log import logging
from framework.utils.captcha import create_validate_code as gcode
from framework.decorators import route
from io import BytesIO
from flask import send_file
from app.conf import msg
from app.untils.format_check import is_mobile
from framework.db import db
collection = db['mongodb']



@route("/register/person", methods=['GET', 'POST'])
def person_register():
    params = request.params
    # 检测手机号格式
    if is_mobile(params['mobile']) is not None:
        return get_ret(msg.PARAMS_ERR)
    if account.is_exists({'_id': params['username']}) or account.is_exists({'_id': params['mobile']}):
        return get_ret(msg.A_EXIST)
    result = account.person_register(params)
    if result.code != 0:
        return get_ret(result)
    username = params['mobile']
    token = account.generate_token(username)
    resp = build_ret(success=True, data=username)
    response = make_response(resp)
    response.headers['Access-Control-Expose-Headers'] = "Authorization"
    response.headers['Authorization'] = token
    account.del_user_err(params['username'])
    return response


@route("/login/person", methods=['GET', 'POST'])
def person_login():
    params = request.params
    if account.get_user_err(params['username']) >= web['pwd_err_freeze']:
        return get_ret(msg.A_LOGIN_MAX)
    account_login_info = account.is_exists({'_id': params['username']})
    if account_login_info:
        if account.valid_pwd(account_login_info['info_id'],pwd=params['pwd']):
            token = account.generate_token(params['username'])
            user_info = collection['UserInfo'].find_one(account_login_info['info_id'])
            username = user_info['username']
            resp = build_ret(success=True,data=username)
            response = make_response(resp)
            response.headers['Access-Control-Expose-Headers'] = "Authorization"
            response.headers['Authorization'] = token
            account.del_user_err(params['username'])
            return response
        else:
            return __check_result_(params['username'])
    return get_ret(msg.A_NO_EXIST)


@route("/logout/person", methods=['GET', 'POST'])
def logout():
    token = request.headers.get('Authorization')
    if account.delete_token_key(token):
        return get_ret(msg.SUCCESS)


@route("/register/company", methods=['GET', 'POST'])
def person_register():
    params = request.params
    # 检测手机号格式
    if is_mobile(params['mobile']) is not None:
        return get_ret(msg.PARAMS_ERR)
    if account.is_exists({'_id': params['username']}) or account.is_exists({'_id': params['mobile']}):
        return get_ret(msg.A_EXIST)
    result = account.company_register(params)
    if result.code != 0:
        return get_ret(result)
    username = params['mobile']
    token = account.generate_token(username)
    resp = build_ret(success=True, data=username)
    response = make_response(resp)
    response.headers['Access-Control-Expose-Headers'] = "Authorization"
    response.headers['Authorization'] = token
    account.del_user_err(params['username'])
    return response


def __verify_captcha__(params, captcha_uuid):
    if account.get_user_err(params['email']) < web['pwd_err_code']:
        return True
    captcha = account.get_captcha(captcha_uuid)
    if str(params['captcha']).lower() != str(captcha).lower():
        return False
    return True


def __check_result_(username):
    counts = account.add_user_err(username)
    if counts >= web['pwd_err_code']:
        return get_ret(msg.A_LOGIN_MAX)
    else:
        return get_ret(msg.A_LOGIN_ERR)