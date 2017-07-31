# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/30 10:27
"""


class ConfigError(Exception):
    def __init__(self, config_name, err={"key_name": "", "key_path": "", "msg": ""}):
        """
        配置文件校验失败
        :param config_name: type(str)
        :param err: type(dict) {"key_name":"", "key_path": "", "msg":""}
        """
        msg = "config validate error. please checking your [%s]! key:[%s], msg:[%s]" % (
            config_name, err['key_path'] + "." + err['key_name'], err['msg'])
        Exception.__init__(self, msg)
