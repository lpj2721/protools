# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/29 11:06
"""


class ERROR(object):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


# global params
SUCCESS = ERROR(0, "操作成功")
FAIL = ERROR(1, "操作失败")
PARAMS_ERR = ERROR(1001, "请求参数不合法")
INVALID_REQUEST = ERROR(1002, "请求已过期")

# sms_code
A_MAX_REQUEST = ERROR(2001, "请求频繁，稍后再试")
A_SMS_ERR = ERROR(2002, "短信平台拒绝服务")
A_CODE_ERR = ERROR(2003, "验证码错误")
A_CODE_TIMEOUT = ERROR(2004, "验证码已失效")

# register
A_EXIST = ERROR(3001, "该账户已经注册")
A_PWD_ERR = ERROR(3002, "两次密码不一致")
A_LOGIN_ERR = ERROR(3003, "用户名或密码错误")
A_NO_EXIST = ERROR(3004, "用户不存在")
A_LOGIN_MAX = ERROR(3005, "用户或密码达到错误次数达到最大上限，冻结用户10分钟")