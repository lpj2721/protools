#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/27 17:56
"""
from db_pool import engine
from db_logs import *

db_pool = engine()


def test_add():
    return "aaa"

__all__ = (
    'db_pool',
)

