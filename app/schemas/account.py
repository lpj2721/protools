#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/6/30 11:36
"""
from framework.schemas import app_schema_request

app_schema_request['/register/person'] = {
    "mobile": {
        "type": "string",
        "format": "phone"
    },
    "pwd": {"type": "string"},
    "re_pwd": {"type": "string"},
    "code":{"type": "string"}
}

app_schema_request['/account/login'] = {
    "username": {
        "type": "string"
    },
    "pwd": {"type": "string"}
}

app_schema_request['/account/get_salt'] = {
    "email": {
        "type": "string",
        "format": "email"
    }
}

app_schema_request['/account/update'] = {
    "name": {"type": "string"},
    "phone": {
        "type": "string",
        "format": "phone"
    },
    "address": {"type": "string"},
    "city": {"type": "string"},
    "province": {"type": "string"},
    "company": {"type": "string"},
    "not_required": ["name", "phone", "address", "city", "province", "company"]
}

app_schema_request['/account/change_passwd'] = {
    "old_pwd": {"type": "string"},
    "new_pwd": {"type": "string"},
    "salt": {"type": "string"}
}

app_schema_request['/account/emailverify'] = {
    "v": {"type": "string"}
}

app_schema_request['/account/delete'] = [
    {
        "type": "string"
    }
]

app_schema_request['/account/test_connection'] = {
    "ip": {
        "type": "string",
        "format": "ipv4"
    },
    "user_name": {"type": "string"},
    "passwd": {"type": "string"}
}

app_schema_request['/account/re_send_email'] = {
    "email": {
        "type": "string",
        "format": "email"
    }
}

app_schema_request['/account/forgot_password'] = {
    "email": {
        "type": "string",
        "format": "email"
    }
}

app_schema_request['/account/reset_passwd'] = {
    "v": {"type": "string"},
    "passwd": {"type": "string"},
    "salt": {"type": "string"}
}

app_schema_request['/account/code'] = {
    "captcha_uuid": {"type": "string"}
}
