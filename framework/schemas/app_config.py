# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/29 15:20
"""

schema_config = dict()
schema_config['log'] = {
    "name": {"type": "string"},
    "level": {"type": "string", "enum": ["debug", "info", "warning", "error", "fatal"]},
    "console": {"type": "boolean"},
    "format": {"type": "string"},
    "file": {
        "enable": {"type": "boolean"},
        "path": {"type": "string"}
    },
    "syslog": {
        "enable": {"type": "boolean"},
        "ip": {"type": "string", "format": "ipv4"},
        "port": {"type": "integer", "maximum": 65535, "minimum": 1},
        "facility": {"type": "string", "pattern": "local[0-7]"}
    }
}

schema_config['email'] = {
    "smtp_addr": {"type": "string"},
    "from_email": {"type": "string", "format": "email"},
    "from_email_pwd": {"type": "string"},
    "subject": {"type": "string"}
}

schema_config['web'] = {
    "url_pre": {"type": "string"},
    "ip": {"type": "string", "format": "ipv4"},
    "port": {"type": "integer", "maximum": 65535, "minimum": 1},
    "session_timeout": {"type": "integer"}
}
