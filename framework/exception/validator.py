# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/31 10:35
"""


class ValidateError(Exception):
    pass


class JSONValidateError(ValidateError):
    def __init__(self, err={"key_name": "", "key_path": "", "msg": ""}):
        """
        JSON校验失败
        :param err: type(dict) {"key_name":"", "key_path": "", "msg":""}
        """
        msg = "JSON格式错误. key:[%s], msg:[%s]" % (err['key_path'] + "." + err['key_name'], err['msg'])
        ValidateError.__init__(self, msg)