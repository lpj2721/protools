# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/24 16:46
"""

import pytest
from mock import Mock

from framework.db.mongo_command import *

collection_mock = Mock()


def test_add():
    data = {"_id": ""}
    add(data, collection_mock)
    collection_mock.insert_one.assert_called_with(data)


def test_add_many():
    data = {"_id": ""}
    add_many(data, collection_mock)
    collection_mock.insert.assert_called_with(data)


def test_update():
    cond = {"_id": ""}
    new = {"xx": ""}
    update(cond, new, collection_mock, unique=True)
    collection_mock.update_one.assert_called_with(cond, {"$set": new})
    update(cond, new, collection_mock, unique=False)
    collection_mock.update.assert_called_with(cond, {"$set": new})


def test_delete():
    cond = {"_id": ""}
    delete(cond, collection_mock, unique=True)
    collection_mock.delete_one.assert_called_with(cond)
    delete(cond, collection_mock, unique=False)
    collection_mock.delete_many.assert_called_with(cond)


def test_get():
    cond = {"_id": ""}
    page = 3
    limit = 30
    collection_mock.find.count.return_value = 10
    collection_mock.find().skip().limit.return_value = []
    get(cond, page, limit, collection_mock)
    collection_mock.find.assert_called_with(cond)
    collection_mock.find().skip.assert_called_with((page - 1) * limit)
    collection_mock.find().skip().limit.assert_called_with(limit)


if __name__ == '__main__':
    pytest.main()
