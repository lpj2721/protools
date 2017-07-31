# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/22 15:33
"""
import sys
from flask_cors import CORS
from app.conf.config import *
from framework.flask import app
from optparse import OptionParser, make_option

from framework.schemas import app_schema_config
from framework.validator import JValidator
from app.conf.config import *


def check_config():
    validator = JValidator(app_schema_config)
    for config in validator.schema.keys():
        from framework.exception import ConfigError

        correct, err = validator.validate(eval(config), config)
        if not correct:
            raise ConfigError(config_name=config, err=err)

if __name__ == '__main__':
    """
    app.debug=True时，定时任务或其他脚本会被执行了2次，原因是flask会多开一个线程来监测项目的变化
    解决方案可以将app.dubug修改为False或添加参数use_reloader=False
    """
    check_config()
    if web['debug']:
        CORS(app, supports_credentials=True)
        app.run(host=web['ip'], port=web['port'], debug=True,threaded=True)
    else:
        app.run(host=web['ip'], port=web['port'])
