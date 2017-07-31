# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: kingsonl@163.com
@time: 2017/3/31 11:19
"""
import time, datetime
from framework.flask import app
from flask import request, make_response
from framework.db import db
from app.conf.config import web, red_pre
from framework.utils import logging
from framework.utils.common import get_ret, md5
from framework.utils.common import get_uuid, get_ret
from app.models import account
import json
from app.conf import msg
from jot import jwt, jws

r = db['redis']
# 不需要登录的操作列表
no_login_list = ['/login/person', '/register/person', '/img/code', '/category', '/brand/add', '/kitchen', '/register/company',
                 '/image', '/province', '/company','/cateblock','/production','/attraction','/company/info',
                 '/province/company', '/register_sms/person', '/news/list', '/news/add', '/partner/add',
                 '/partner/list', '/ProductionBase/add', '/ProductionBase/list', '/ProductionBase/detail', '/notice/add', '/notice/list','/production','/news/detail','/notice/detail'
                 ]
no_login = []


def make_rule(prefix, api_vers, no_login_list):
    for index in range(len(no_login_list)):
        if not prefix.endswith("/"):
            prefix += "/"
        for api in api_vers:
            no_login.append(prefix + api + no_login_list[index])


make_rule(web['url_pre'], web['api_version'], no_login_list)


@app.before_request
def before_request():
    # check permission
    if not __check_permission__():
        # check sign
        return __verify_sign__()


def __check_login__(token):
    """
    platform兼容各平台
    统计总平台与各平台设备hgetall,
    通过placeholder来限制各平台设备数
    备注：映射关系 {email + platform + place --> ssid}无法设置过期时间，
    当APP内用户量庞大时需要定时清理ssid为None的epp映射关系，一期暂时不做清理
    :return:
    """
    key_pix = r.get(token)
    if key_pix:
        # 是否注销登录
        no_valid_token = jwt.decode(token, signers=[jws.HmacSha(bits=256, key=web['token_key']+key_pix)])
        # 校验token是否有效
        if no_valid_token['valid']:
            now_timestamp = time.time()
            if no_valid_token['payload']['exp'] > now_timestamp:
                return no_valid_token['payload']['username']
            else:
                r.delete(token)
                return False
        else:
            r.delete(token)
            return False
    else:
        return False


def __check_permission__():
    path = request.path
    # session time out
    if request.method == "GET":
        return True
    if path in no_login:
        return True
    return False


def __verify_sign__():
    """
    验签sign=md5(ssid + username + platform + timestamp + path + params)
    :return:
    """
    token = str(request.headers.get('Authorization'))
    # is login
    username = __check_login__(token)
    if username:
        params = ''
        request.user_name = username
        if request.params:
            params = json.dumps(request.params, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
        #
        logging.info("token:[%s], username:[%s], params:[%s]"
                     % (token, username, str(params)))
    else:
        return get_ret(msg.INVALID_REQUEST)

#
# if __name__ == '__main__':
#     print r.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjE1MTcwNDUwNjcxIiwiaWF0IjoxNDk5OTE2NDg5LjcwMywiZXhwIjoxNDk5OTIzNjg5LjcwM30.Sg8mkd9kXGQ2FvOyEMmPRhqepvdIVD5ygkreDVwvAOE")
