#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/6/30 17:34
"""
from flask import request
from framework.decorators import route
from app.conf.config import web
from app.conf import msg
from framework.utils.common import get_ret
from framework.utils.log import logging
from app.untils.format_check import is_mobile
from app.models.valid_code import send_sms
from app.models import account
from framework.utils.captcha import create_validate_code as gcode
from io import BytesIO
from flask import send_file,make_response


@route("/register_sms/person", methods=['GET', 'POST'])
def register_sms_person():
    params = request.params
    # 检测手机号格式
    if is_mobile(params['mobile']) is not None:
        return get_ret(msg.PARAMS_ERR)
    # 检测手机号是否已注册
    if account.is_exists(dict(_id=params['mobile'])):
        return get_ret(msg.A_EXIST)
    sms_response = send_sms(params['mobile'])
    return get_ret(sms_response)


@route("/img/code", methods=['GET', 'POST'])
def generate_code():
    code_img = gcode()
    params = request.params
    logging.info("生成的验证码为[%s]", code_img[1])
    return __mk_captcha__(params['captcha_uuid'], code_img)


def __mk_captcha__(captcha_uuid, code_img):
    byte_io = BytesIO()
    code_img[0].save(byte_io, 'PNG')
    byte_io.seek(0)
    account.add_code_redis(captcha_uuid, code_img[1])
    response = make_response(send_file(byte_io, mimetype='image/png', cache_timeout=0))
    # 添加跨域返回自定义字段
    # response.headers['Access-Control-Allow-Origin'] = "*"
    # response.headers['Access-Control-Allow-Methods'] = "POST, GET"
    # response.headers['captcha_uuid'] = uuid
    # response.headers['Access-Control-Expose-Headers'] = "captcha_uuid"
    return response