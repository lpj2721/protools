#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/1 15:59
"""
from framework.schemas import app_schema_request

app_schema_request['/register_sms/person'] = {
    "mobile": {
        "type": "string"
    }
}


app_schema_request['/img/code'] = {
    "captcha_uuid": {
        "type": "string"
    }
}