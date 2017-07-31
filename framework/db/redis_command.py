# encoding: utf-8
"""
@version: 1.0
@author: kelvin
@contact: kingsonl@163.com
@time: 2017/3/29 14:48
"""

#
# class credis:
#     def __init__(self, r):
#         self.r = r
#
#     def set(self, key, value, ex=None):
#         """
#         设置值,如存在则覆盖
#         :param key: type(String)
#         :param value: type(object)
#         :param ex: type(int) 存储时间
#         :return:
#         """
#         return self.r.set(key, value, ex=ex)
#
#     def delete(self, *name):
#         """
#         删除一个或多个指定的name
#         :param name: type(String)
#         :return:
#         """
#         return self.r.delete(*name)
#
#     def get(self, key):
#         """
#         返回该key的值,如不存在则返回None
#         :param key: type(String)
#         :return:
#         """
#         return self.r.get(key)
#
#     def incr(self, key, amount=1):
#         """
#         将 key 中储存的数字值增一
#         :param key: type(String)
#         :param amount: type(int)
#         :return:
#         """
#         self.r.incr(key, amount)
#
#     def expire(self, name, ex=None):
#         """
#         给某个name设置有效时间
#         :param name:
#         :param ex:
#         :return:
#         """
#         if ex is not None:
#             return self.r.expire(name, ex)
#
#     def exists(self, key):
#         """
#         判断key是否存在
#         :param key: type(String)
#         :return: 返回True or False
#         """
#         return self.r.exists(key)
#
#     def hexists(self, key, name):
#         """
#         判断key,value是否存在
#         :param key: type(String)
#         :param name: type(String)
#         :return: 返回True or False
#         """
#         return self.r.hexists(name, key)
#
#     def hset(self, name, key, value, ex=None):
#         """
#         用于为哈希表中的字段赋值,如存在则覆盖
#         :param name: type(String)
#         :param key: type(String)
#         :param value: type(object)
#         :return: 创建返回1 存在返回0
#         """
#         self.r.hset(name, key, value)
#         self.expire(name, ex)
#
#     def hget(self, name, key):
#         """
#         用于返回哈希表中指定字段的值
#         :param key: type(String)
#         :return:
#         """
#         return self.r.hget(name, key)
#
#     def hdel(self, name, *key):
#         """
#         删除哈希表 key 中的一个或多个指定字段
#         :param name: type(String)
#         :param key: type(String)
#         :return:
#         """
#         return self.r.hdel(name, *key)
#
#     def hgetall(self, name):
#         """
#         用于返回哈希表中，所有的字段和值
#         :param name: type(String)
#         :return: 返回dict('key':'value')
#         """
#         return self.r.hgetall(name)
#
#     def hmset(self, name, mapping, ex=None):
#         """
#         用于同时将多个 field-value (字段-值)对设置到哈希表中
#         :param name: type(String)
#         :param mapping: type(dict)
#         :param ex: type(int) 存储时间毫秒
#         :return:
#         """
#         self.r.hmset(name, mapping)
#         self.expire(name, ex)
#
#     def hmget(self, name, keys, *args):
#         """
#         用于返回哈希表中，一个或多个给定字段的值
#         :param name: type(String)
#         :param keys: type(list)
#         :param args: type(list)
#         :return:
#         """
#         return self.r.hmget(name, keys, args)
#
#     def rpush(self, name, *values):
#         """
#         用于将一个或多个值插入到列表的尾部(最右边)
#         :param name: type(String)
#         :param values: type(object)
#         :return:
#         """
#         return self.r.rpush(name, values)
#
#     def lrange(self, name, start, end):
#         """
#         回列表中指定区间内的元素,区间以偏移量 START 和 END 指定。 其中 0 表示列表的第一个元素
#         :param name: type(String)
#         :param start: type(int)
#         :param end: type(int)
#         :return:
#         """
#         return self.r.lrange(name, start, end)
#
#     def blpop(self, keys):
#         """
#         命令移出并获取列表的第一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止
#         :param keys: type(String)
#         :return:
#         """
#         return self.r.blpop(keys)
#
#     def piplines_set(self, name, value, ex=None):
#         """
#         设置值,如存在则覆盖
#         :param key: type(String)
#         :param value: type(object)
#         :param ex: type(int) 存储时间毫秒
#         :return:
#         """
#         pipe = self.r.pipeline()
#         pipe.set(name, value, ex=ex)
#         return pipe.execute()
#
#     def piplines_hset(self, name, key, value, ex=None):
#         """
#         用于为哈希表中的字段赋值,如存在则覆盖
#         :param name: type(String)
#         :param key: type(String)
#         :param value: type(object)
#         :param ex: type(int) 存储时间毫秒
#         :return:
#         """
#         pipe = self.r.pipeline()
#         pipe.hset(name, key, value)
#         pipe.pexpire(name, ex)
#         return pipe.execute()
#
#     def piplines_hmset(self, name, mapping, ex=None):
#         """
#         用于同时将多个 field-value (字段-值)对设置到哈希表中
#         :param name: type(String)
#         :param mapping: type(dict)
#         :param ex: type(int) 存储时间毫秒
#         :return:
#         """
#         pipe = self.r.pipeline()
#         pipe.hmset(name, mapping)
#         pipe.pexpire(name, ex)
#         return pipe.execute()
