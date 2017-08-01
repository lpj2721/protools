#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/29 17:58
"""
from framework.db import db
import json


class ProductCategory:
    __table_name__ = "product_category"
    _db = db['mongodb'][__table_name__]

    def __init__(self, category_id=None, name=None):
        self._id = category_id
        self.name = name

    def insert(self, kwargs):
        if isinstance(kwargs, dict):
            if self.__dict__.keys() == kwargs.keys():
                print kwargs
                update_result = self._db.insert_one(kwargs)
                if update_result.inserted_id:
                    return True
        else:
            return False

    def update(self, kwargs):
        if isinstance(kwargs, dict):
            kwargs_key = kwargs.keys()
            if self.arg_verify(kwargs_key) or "_id" not in kwargs_key:
                return False
            self._id = kwargs.pop("_id")
            update_result = self._db.update_one(self._id, {"$set":{kwargs}})
            if update_result.upserted_id:
                return True
        else:
            return False

    def is_exist(self, _id):
        pass


    def arg_verify(self,keys):
        cls_key = self.__dict__.keys()
        kwargs_key = keys
        if len(kwargs_key) > len(cls_key) or [key for key in kwargs_key if key not in cls_key]:
            return True

    def insert_arg_verify(self,keys):
        cls_key = self.__dict__.keys()
        kwargs_key = keys
        if len(kwargs_key) > len(cls_key) or [key for key in kwargs_key if key not in cls_key]:
            return True


if __name__ == '__main__':
    s_fun = ProductCategory()
    s_fun.insert({"_id": "123", "name": "sa"})
    print s_fun

