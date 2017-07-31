#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/7/10 11:33
"""
from app.conf.config import web, red_pre
from app.conf import msg
from framework.db import db, mongo_command
from framework.utils.common import get_uuid, date_time
from jot import jwt, jws
import time, string,random
from bson.objectid import ObjectId

collection = db['mongodb']
r = db['redis']

def news_add(params):
    create_time = date_time()
    info_data = {
        '_id': get_uuid(),
        'title': params['title'],
        'subtitle': params['subtitle'],
        'abstract': params['abstract'],
        'contents': params['contents'],
        'pictures': params['pictures'],
        'type': params['type'],
        'area': params['area'],
        'source': params['source'],
        'province': params['province'],
        'city': params['city'],
        'create_time': create_time
    }
    info_id = collection['MediaNews'].insert_one(info_data).inserted_id
    if info_id:
        return True
    else:
        return False

def news_list(cond, page=0, limit=10):
    """
    :param cond: type(dict) 查询条件条件
    :param page: type(num) 查询页码
    :param limit: type(num) 查询条数
    :return: data,total
    """
    return mongo_command.get(collection['MediaNews'], cond, page, limit, projection=None)

def news_detail(id):
    """
    :param cond: type(dict) 查询条件条件
    :return: data
    """
    cond = {
        "_id":id
    }
    return mongo_command.get_one(collection['MediaNews'], cond, projection=None)

def notice_add(params):
    create_time = date_time()
    info_data = {
        '_id': get_uuid(),
        'title': params['title'],
        'contents': params['contents'],
        'type': params['type'],
        'create_time': create_time
    }
    info_id = collection['Notice'].insert_one(info_data).inserted_id
    if info_id:
        return True
    else:
        return False

def notice_list(cond, page=0, limit=10):
    """
    :param cond: type(dict) 查询条件条件
    :param page: type(num) 查询页码
    :param limit: type(num) 查询条数
    :return: data,total
    """
    return mongo_command.get(collection['Notice'], cond, page, limit, projection=None)

def notice_detail(id):
    """
    :param cond: type(dict) 查询条件条件
    :return: data
    """
    cond = {
        "_id": id
    }
    return mongo_command.get_one(collection['Notice'], cond, projection=None)