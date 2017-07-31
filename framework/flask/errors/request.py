# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/29 11:02
"""
import traceback

from app.conf import web
from framework.flask import app

from framework.exception.validator import JSONValidateError
from framework.utils import build_ret
from framework.utils import logging


# 异常统一处理
@app.errorhandler(JSONValidateError)
def json_validate_error(e):
    response = build_ret(False, msg=e.message)
    logging.error(traceback.format_exc(e))
    return response


@app.errorhandler(Exception)
def internal_error(e):
    if web['debug']:
        response = build_ret(False, msg=e.message)
    else:
        response = build_ret(False, msg="意外错误")
    logging.error(traceback.format_exc(e))
    return response


# 处理404页面
@app.errorhandler(404)
def not_found(e):
    response = build_ret(False, msg="页面不存在")
    return response


# 处理400页面
@app.errorhandler(400)
def bad_request(e):
    response = build_ret(False, msg="请求错误")
    logging.error(traceback.format_exc(e))
    return response
