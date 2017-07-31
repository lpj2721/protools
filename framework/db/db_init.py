# encoding: utf-8

"""
@version: 1.0
@author: emrick
@contact: emrick@163.com
@time: 2017/3/29 11:10
"""
import re

from app.conf.config import db_type, dbs, mysql_pool_config, mongo_pool_config, redis_pool_config

"""
静态资源初始化脚本
"""


def _init_db(dbs):
    if _validate_dbs_config(dbs_config=dbs):
        db = {}
        for db_key in dbs.iterkeys():
            _type = dbs[db_key]['type']
            if _type == db_type['mongodb']:
                db[db_key] = _get_mongo(dbs[db_key])
            if _type == db_type['mysql']:
                db[db_key] = _get_mysql(dbs[db_key])
            if _type == db_type['redis']:
                db[db_key] = _get_redis(dbs[db_key])
        return db
    else:
        raise Exception("config.dbs 配置有误")


def _get_mongo(mongo_config):
    from pymongo import MongoClient
    if mongo_config['pool_size'] == 0:
        __mongo = MongoClient(mongo_config['host'], mongo_config['port'])
        mongo_db = __mongo[mongo_config['db_name']]
    else:
        config = mongo_pool_config
        config['minPoolSize'] = mongo_config['pool_size']
        config['host'] = mongo_config['host']
        config['port'] = mongo_config['port']
        __mongo = MongoClient(**config)
        mongo_db = __mongo[mongo_config['db_name']]
    if mongo_config['user_name'] != "" or mongo_config['password'] != "":
        mongo_db.authenticate(mongo_config['user_name'], mongo_config['password'])
    return mongo_db


def _get_mysql(mysql_config):
    import pymysql
    from DBUtils import PooledDB
    if mysql_config['pool_size'] == 0:
        __mysql = pymysql.connect(host=mysql_config['host'], user=mysql_config['user_name'],
                                  passwd=mysql_config['password'],
                                  port=mysql_config['port'], db=mysql_config['db_name'], charset="utf8")
        if not __mysql:
            from pymysql import MySQLError
            raise MySQLError("数据库连接失败")
        return DbObject(connection=__mysql)
    else:
        config = mysql_pool_config
        config['mincached'] = mysql_config['pool_size']
        config['host'] = mysql_config['host']
        config['user'] = mysql_config['user_name']
        config['passwd'] = mysql_config['password']
        config['port'] = mysql_config['port']
        config['db'] = mysql_config['db_name']
        pool = PooledDB.PooledDB(pymysql, **config)
        if not pool:
            from DBUtils.PooledDB import PooledDBError
            raise PooledDBError("连接池初始化失败")
        return DbObject(pool=pool)


def _get_redis(redis_config):
    import redis
    if redis_config['pool_size'] == 0:
        if redis_config['password'] == '':
            r = redis.StrictRedis(host=redis_config['host'], port=redis_config['port'])
        else:
            r = redis.StrictRedis(host=redis_config['host'], port=redis_config['port'],
                                  password=redis_config['password'])
    else:
        config = redis_pool_config
        config['host'] = redis_config['host']
        config['port'] = redis_config['port']
        config['max_connections'] = redis_config['pool_size']
        pool = redis.ConnectionPool(**config)
        if redis_config['password'] == '':
            r = redis.StrictRedis(connection_pool=pool)
        else:
            r = redis.StrictRedis(connection_pool=pool, password=redis_config['password'])
    return r


def _validate_dbs_config(dbs_config):
    """
    校验数据库配置 config->dbs 数据
    :param dbs_config:
    :return:
    """
    type_pattern = ''
    for _type in db_type.itervalues():
        type_pattern += "^" + _type + "$|"
    type_pattern = type_pattern[0:len(type_pattern) - 1]
    type_pattern = r'({})'.format(type_pattern)
    validate_config = {
        'type': type_pattern,
        'host': r'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))',
        'port': r'([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-5]{2}[0-3][0-5])',
        'pool_size': r'\d*',
        'user_name': r'\w*',
        'password': r'\w*',
        'db_name': r'\w*'
    }
    validate = True
    for db_key in dbs_config.iterkeys():
        db_config_keys = dbs_config[db_key].iterkeys()
        if not cmp(validate_config.iterkeys(), db_config_keys):
            validate = False
        for db_config_key in db_config_keys:
            if not re.match(validate_config[db_config_key], str(dbs_config[db_key][db_config_key])):
                validate = False
    return validate


db = _init_db(dbs=dbs)


class DbObject:
    def __init__(self, pool=None, connection=None):
        self.pool = pool
        self.connection = connection
        self.cursor = None

    def __enter__(self):
        if self.pool:
            self.connection = self.pool.connection()
            self.cursor = self.connection.cursor()
        else:
            if not self.connection:
                raise ValueError("pool和conection不能同时为None")
            else:
                self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.cursor:
            self.cursor.close()
        if not self.connection:
            self.connection.close()

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor
