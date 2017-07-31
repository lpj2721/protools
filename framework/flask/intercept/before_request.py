# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/31 9:42
"""
import json as JSON

from flask import request, abort

from app.conf.config import web
from framework.exception.validator import JSONValidateError
from framework.flask import app
from framework.schemas import app_schema_request
from framework.utils import logging
from framework.validator import JValidator

validator = JValidator(app_schema_request)


@app.before_request
def before_request():
    if request.path:
        do_something()


def do_something():
    request.params = get_request_args()
    url = str(request.url)
    # get ip
    ip = request.headers.get('X-Real-IP')
    if ip is None or ip == '':
        ip = "127.0.0.1"
    logging.info( 'ip: %2s request url is: [%s], input is: [%s]',ip, url, request.params)
    api_version, real_path = parse_path(request.path, web['url_pre'], web['api_version'])
    request.api_version = api_version
    validate_json(real_path)


def get_request_args():
    json = {}
    if request.method == "GET":
        json = request.args.to_dict()
        # parse json
        for k, v in json.items():
            if json[k].startswith("{"):
                json[k] = JSON.loads(v)
    elif request.method == "POST":
        json = request.data
        if json is not None and json != '':
            try:
                json = JSON.loads(json)
            except ValueError:
                pass
    return json


def validate_json(schema_name):
    if schema_name in validator.schema.keys():
        correct, err = validator.validate(json=request.params, schema_name=schema_name)
        if not correct:
            raise JSONValidateError(err)


def parse_path(path, prefix, api_version):
    """
    处理url路径
    :param path: 路径
    :param prefix: 前缀
    :param api_version: api版本集合
    :return: (type(str), type(str)) 例如
    parse_path("/api/cloud/v1/template/add", "/api/cloud", True) = ("v1", "/template/add")
    """
    prefix_fixed = prefix
    if not prefix.startswith("/"):
        prefix_fixed = "/" + prefix
    if prefix.endswith("/"):
        prefix_fixed = prefix_fixed[:-1]
    if not path.startswith(prefix_fixed):
        return "", ""
    path_with_api = path.replace(prefix_fixed, "", 1)
    if path_with_api.startswith("/"):
        path_with_api = path_with_api[1:]
    if api_version:
        parts = path_with_api.partition("/")
        api_version = parts[0]
        real_path = "/" + parts[2]
        return api_version, real_path
    else:
        return "", "/" + path_with_api
