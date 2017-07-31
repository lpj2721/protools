#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/27 20:59
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from app.mysql_db import db_pool
ModelBase = declarative_base()  # <-元类


class User(ModelBase):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True)
    date_joined = Column(DateTime)
    username = Column(String(length=30))
    password = Column(String(length=128))


class ProductCategory(ModelBase):
    __tablename__ = "product_category"
    category_id = Column(Integer, primary_key=True, autoincrement=True, comment= u"商品分类id")
    name = Column(String(50), nullable=False, default=u"分类名称")

ModelBase.metadata.drop_all(bind=db_pool)
print 123
ModelBase.metadata.create_all(bind=db_pool)