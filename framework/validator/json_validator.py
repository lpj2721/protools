# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/27 17:11
"""
import jsonschema
from jsonschema import SchemaError
from jsonschema import ValidationError


class JValidator(object):
    """
    JSON校验类
    """
    NOT_REQUIRED_KEY = 'not_required'
    OBJ_EXCLUDE_KEYS = [NOT_REQUIRED_KEY]
    TYPE_VALUES = ['null', 'boolean', 'integer', 'number', 'string']
    schema = {}

    def __init__(self, schema_config):
        """
        初始化校验器
        :param schema_config: 校验器字典 格式如下：json_Validator[`url`] = `schema`
        :return:
        :type schema_config: dict
        """
        self.schema = schema_config
        for k, v in schema_config.items():
            schema_config[k] = self.make_schema(v)

    def make_schema(self, schema_config):
        """
        根据schema的配置生成符合jsonschema语法的配置文件
        :param schema_config:
        :return: jsonschema
        :type schema_config: dict
        :rtype dict
        """
        schema = self.make_schema_helper(schema_config)
        schema['$schema'] = "http://json-schema.org/schema#"
        return schema

    def validate(self, json, schema_name):
        """
        校验方法
        :param json: type(str) 请求json
        :param schema_name: type(str) schema名称
        :return: (boolean, dict)
                如果校验通过返回 (True, );如果校验不通过 (False, err)
                err = {
                    "key_name":"",
                    "key_path":"",
                    "msg": ""
                }
        :type json: dict
        :type schema_name: str
        :rtype (bool, str)
        """
        err = {
            "key_name": "",
            "key_path": "",
            "msg": ""
        }
        try:
            jsonschema.validate(json, self.schema[schema_name], format_checker=jsonschema.FormatChecker())
            return True, err
        except ValidationError, e:
            key_name = ""
            if e.path:
                key_name = e.path.pop().replace(".", "")
            key_path = str(list(e.path)).replace("[", "").replace("]", "").replace(", ", ".").replace("'", "")
            msg = e.message
            err['key_name'] = key_name
            err['key_path'] = key_path
            err['msg'] = msg
            return False, err
        except SchemaError:
            raise SchemaError("invalid schema in validator[%s], please checking" % schema_name)
        except KeyError:
            raise ValueError("not found schema name [%s] in schema config" % schema_name)

    def make_schema_helper(self, schema_config):
        schema = {}
        if self.is_array(schema_config):
            schema['type'] = 'array'
            if len(schema_config) is 2:
                schema['items'] = self.make_schema_helper(schema_config[0])
                array_setting = schema_config[1]
                schema = dict(schema, **array_setting)
        elif self.is_config(schema_config):
            schema = schema_config
        else:
            schema['type'] = 'object'
            schema['properties'] = {}
            for k, v in schema_config.items():
                if k not in self.OBJ_EXCLUDE_KEYS:
                    schema['properties'][k] = self.make_schema_helper(v)
            not_req = []
            if self.have_not_required_key(schema_config):
                not_req = schema_config.pop(self.NOT_REQUIRED_KEY)
            schema['required'] = self.make_required(not_req, schema_config)
            if not schema['required']:
                schema.pop('required')
        return schema

    @staticmethod
    def is_array(obj):
        return isinstance(obj, list)

    def is_config(self, obj):
        return obj.get('type', '') in self.TYPE_VALUES

    def have_not_required_key(self, schema_config):
        return self.NOT_REQUIRED_KEY in schema_config.keys()

    @staticmethod
    def make_required(not_req, schema_config):
        lst = []
        for k in schema_config.keys():
            if k not in not_req:
                lst.append(k)
        lst.sort()
        return lst
