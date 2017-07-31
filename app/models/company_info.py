#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/21 17:04
"""
from framework.db import db
collection = db['mongodb']


def company_info(username):
    user_info = collection['UserLoginInfo'].find_one(username)
    company_id = collection['UserInfo'].find_one(user_info['info_id'])['company']
    company = collection['CompanyInfo'].find_one(company_id)
    return company