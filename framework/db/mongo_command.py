# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/24 15:57
"""

"""通用数据库操作函数"""


def get(collection, cond, page=0, limit=0, projection=None):
    """
    分页查询方法
    :param cond: 查询条件
    :param page: 页
    :param limit: 每页多少条
    :param collection: 
    :param projection: 展示字段，默认_id显示{'name': 1, _id: 0}
    :return: 数据和总数
    :type cond: dict
    :type page: int
    :type limit: int
    :type collection: MongoDB.collection
    :type projection: dict
    :rtype (list, int)
    """
    find_cursor = collection.find(cond, projection=projection)
    total = find_cursor.count()
    cursor = find_cursor.skip((page - 1) * limit).limit(limit)
    data = []
    # ObjectId to str
    for x in cursor:
        data.append(x)
    return data, total


def get_one(collection, cond, projection=None, throwable=None):
    """
    获取一条记录
    :param collection:
    :param cond: 条件
    :param projection: type(dict) 展示字段，默认_id显示{'name': 1, _id: 0}
    :param throwable: 异常对象
    :return:
    :type collection: MongoDB.collection
    :type cond: dict
    :type projection: dict
    :type throwable: Exception
    :rtype dict
    """
    result = collection.find_one(cond, projection=projection)
    if result is None and throwable:
        raise throwable
    return result
