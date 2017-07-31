# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/27 17:12
"""

import pytest
from jsonschema import SchemaError
from jsonschema.validators import validator_for

from framework.validator.json_validator import JValidator

config_with_simple_json = {
    "opr": {
        "type": "string",
        "enum": ["collection", "pay_for"]
    }
}

schema_with_simple_json = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "opr": {"type": "string", "enum": ["collection", "pay_for"]}
    }
}

config_with_array = {
    "opr": {
        "type": "string",
        "enum": ["collection", "pay_for"]
    },
    "item": [{
        "bank_account": {"type": "string", "maxLength": 19, "maxLength": 19},
        "bank_account_name": {"type": "string", "maxLength": 10, "maxLength": 4}
    }, {
        "maxLength": 5,
        "minLength": 1
    }]
}
schema_with_array = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "opr": {"type": "string", "enum": ["collection", "pay_for"]},
        "item": {
            "type": "array",
            "maxLength": 5,
            "minLength": 1,
            "items": {
                "type": "object",
                "properties": {
                    "bank_account": {"type": "string", "maxLength": 19, "maxLength": 19},
                    "bank_account_name": {"type": "string", "maxLength": 10, "maxLength": 4}
                }
            }
        }
    }
}

config_with_not_required = {
    "opr": {"type": "string", "enum": ["collection", "pay_for"]},
    "account": {"type": "string", "maxLength": 10, "minLength": 1},
    "remark": {"type": "string"},
    "user_name": {"type": "integer", "maximum": 99999, "minimum": 10000},
    "realtime": {"type": "integer", "enum": [0, 1]},
    "agreement_id": {"type": "string", "maxLength": 16, "maxLength": 16},
    "not_required": ["remark", "realtime"]
}
schema_with_not_required = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "opr": {"type": "string", "enum": ["collection", "pay_for"]},
        "account": {"type": "string", "maxLength": 10, "minLength": 1},
        "remark": {"type": "string"},
        "user_name": {"type": "integer", "maximum": 99999, "minimum": 10000},
        "realtime": {"type": "integer", "enum": [0, 1]},
        "agreement_id": {"type": "string", "maxLength": 16, "maxLength": 16}
    },
    "required": ['account', 'agreement_id', 'opr', 'user_name']
}

config_with_nest_json = {
    "opr": {"type": "string", "enum": ["collection", "pay_for"]},
    "account": {"type": "string", "maxLength": 10, "minLength": 1},
    "user": {
        "username": {"type": "string"},
        "password": {"type": "integer", "maximum": 999999, "minimum": 100000}
    }
}
schema_with_nest_json = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "opr": {"type": "string", "enum": ["collection", "pay_for"]},
        "account": {"type": "string", "maxLength": 10, "minLength": 1},
        "user": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "integer", "maximum": 999999, "minimum": 100000}
            }
        }
    }
}

config_with_whole = {
    "opr": {"type": "string", "enum": ["collection", "pay_for"]},
    "account": {"type": "string", "maxLength": 10, "minLength": 1},
    "item": [
        {
            "bank_account": {"type": "string", "maxLength": 19, "minLength": 19},
            "bank_account_name": {"type": "string", "maxLength": 10, "minLength": 4},
            "not_required": ["bank_account_name"]
        }, {
            "maxLength": 5,
            "minLength": 1
        }],
    "user": {
        "username": {"type": "string"},
        "password": {"type": "integer", "maximum": 999999, "minimum": 100000},
        "not_required": ["username"]
    },
    "not_required": ["account"]
}

schema_with_whole = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "opr": {"type": "string", "enum": ["collection", "pay_for"]},
        "account": {"type": "string", "maxLength": 10, "minLength": 1},
        "item": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "bank_account": {"type": "string", "maxLength": 19, "minLength": 19},
                    "bank_account_name": {"type": "string", "maxLength": 10, "minLength": 4}
                },
                "required": ["bank_account"]
            },
            "maxLength": 5,
            "minLength": 1
        },
        "user": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "integer", "maximum": 999999, "minimum": 100000}
            },
            "required": ["password"]
        }
    },
    "required": ["item", "opr", "user"]
}
schema_config = {
    "simple_json": config_with_simple_json,
    "array": config_with_array,
    "not_required": config_with_not_required,
    "nest_json": config_with_nest_json,
    "whole": config_with_whole
}
validator = JValidator(schema_config)


def check(name, correct_schema):
    schema = validator.schema[name]
    cls = validator_for(schema)
    is_valid_schema = True
    try:
        cls.check_schema(schema)
    except SchemaError:
        is_valid_schema = False
    assert is_valid_schema
    assert schema == correct_schema


# 测试单层json
def test_make_schema_with_simple_json():
    check("simple_json", schema_with_simple_json)


# 测试数组对象
def test_make_schema_with_array():
    check("array", schema_with_array)


# 测试not_required对象
def test_make_schema_with_not_required():
    check("not_required", schema_with_not_required)


# 测试嵌套json
def test_make_schema_with_nest_json():
    check("nest_json", schema_with_nest_json)


# 总体测试
def test_make_schema_whole():
    check("whole", schema_with_whole)


if __name__ == '__main__':
    args = ["-vv", "--color", "yes", "test_json_validator.py"]
    pytest.main(args)
