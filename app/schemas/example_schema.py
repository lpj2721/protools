# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/28 15:04
"""
from framework.schemas import app_schema_request

# 这个例子将对接口 /login 的请求json进行校验
# 如需将规则分别添加到不同的文件 直接在该目录下新建py文件然后仿照该例子添加规则即可
app_schema_request['/login'] = {
    "opr": {
        "type": "string",
        "enum": ["collection", "pay_for"]
    }
}
