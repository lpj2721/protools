#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/27 20:22
"""
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from app.conf.config import mysql_pool_configs


def engine():
    db_pool = create_engine(mysql_pool_configs['url'], poolclass=QueuePool)
    return db_pool


# if __name__ == '__main__':
#     a = engine()
#     print 11111
#     print a
#     print id(a)
#     print type(a)



