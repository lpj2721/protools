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

def production_base_add(params):
    create_time = date_time()
    info_data = {
        '_id': get_uuid(),
        'name': params['name'],
        'product': params['product'],
        'province': params['province'],
        'content': params['content'],
        'people': params['people'],
        'certificate': params['certificate'],
        'pic': params['pic'],
        'type': params['type'],
        'city': params['city'],
        'address': params['address'],
        'telephone': params['telephone'],
        'companys': params['companys'],
        'brand': params['brand'],
        'create_time': create_time
    }
    info_id = collection['ProductionBase'].insert_one(info_data).inserted_id
    if info_id:
        return True
    else:
        return False

def production_base_list(cond, page=0, limit=10):
    """
    :param cond: type(dict) 查询条件条件
    :param page: type(num) 查询页码
    :param limit: type(num) 查询条数
    :return: data,total
    """
    return mongo_command.get(collection['ProductionBase'], cond, page, limit, projection=None)

def production_base_detail(id):
    """
    :param id: id 查询条件条件
    :return: data
    """
    cond = {
        "_id": id
    }
    return mongo_command.get_one(collection['ProductionBase'], cond, projection=None)