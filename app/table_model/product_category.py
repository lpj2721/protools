#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/29 17:58
"""
from sqlalchemy import Column, Integer, String, DateTime
from . import ModelBase


class ProductCategory(ModelBase):
    __tablename__ = "product_category"
    category_id = Column(Integer, primary_key=True, autoincrement=True, comment= "商品分类id")
    name = Column(String(50), nullable=False, default=u"分类名称")

    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name
