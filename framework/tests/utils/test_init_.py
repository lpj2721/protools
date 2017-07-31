# encoding: utf-8

"""
@version: 1.0
@author: emrick
@contact: yeemrick@gmail.com
@time: 2017/3/24 17:04
"""

# validate_config = {
#         "mongodb": {
#             "type": "mongodb",
#             "host": "172.18.0.92",
#             "port": 10110,
#             "pool_size": 3,
#             "user_name": "test",
#             "password": "test123456",
#             "db_name": "ylcloud"
#         },
#         "mysql": {
#             "type": "mysql",
#             "host": "255.255.255.255",
#             "port": 3360,
#             "pool_size": 5,
#             "user_name": "test",
#             "password": "test_123456",
#             "db_name": "ylcloud"
#         }
#     }
#
#
# def test_validate_dbs_config():
#     from framework.db import _validate_dbs_config
#     assert _validate_dbs_config(validate_config) == True
#
#
# input_config1 = {
#         "type": "mysql",
#         "host": "172.18.0.92",
#         "port": 3306,
#         "pool_size": 0,
#         "user_name": "test",
#         "password": "test123456",
#         "db_name": "ylcloud"
#     }
# input_config2 = {
#         "type": "mysql",
#         "host": "172.18.0.92",
#         "port": 3306,
#         "pool_size": 3,
#         "user_name": "test",
#         "password": "test123456",
#         "db_name": "ylcloud"
#     }
# input_config3 = {
#         "type": "mysql",
#         "host": "172.18.0.912",
#         "port": 3306,
#         "pool_size": 0,
#         "user_name": "test",
#         "password": "test123456",
#         "db_name": "ylcloud"
#     }
# input_config4 = {
#         "type": "mysql",
#         "host": "172.18.0.92",
#         "port": 3306,
#         "pool_size": 3,
#         "user_name": "tes1t",
#         "password": "test123456",
#         "db_name": "ylcloud"
#     }
#
# @patch("pymysql.connect")
# @patch("DBUtils.PooledDB.PooledDB")
# @pytest.mark.parametrize("input_config", [input_config1, input_config2])
# def test_get_mysql(pooled_mock, connect_mock, input_config):
#     from pymysql import MySQLError
#     from DBUtils.PooledDB import PooledDBError
#     db_config = {
#         "type": "mysql",
#         "host": "172.18.0.92",
#         "port": 3306,
#         "pool_size": 0,
#         "user_name": "test",
#         "password": "test123456",
#         "db_name": "ylcloud"
#     }
#     pool_config = {
#         "type": "mysql",
#         "host": "172.18.0.92",
#         "port": 3306,
#         "pool_size": 3,
#         "user_name": "test",
#         "password": "test123456",
#         "db_name": "ylcloud"
#     }
#     if cmp(db_config, input_config) == 0 or cmp(pool_config, input_config) == 0:
#         connect_mock.return_value = True
#         pooled_mock.return_value = True
#         from framework.db import _get_mysql
#         _get_mysql(db_config)
#         _get_mysql(pool_config)
#     else:
#         connect_mock.return_value = False
#         pooled_mock.return_value = False
#         with pytest.raises(MySQLError):
#             models._get_mysql(db_config)
#         with pytest.raises(PooledDBError):
#             models._get_mysql(pool_config)


# def test_init_db():
#     from utils.const import DB_TYPE
#     dbs = {
#         "mongodb": {
#             "type": DB_TYPE["mongodb"],
#             "host": "10.10.0.100",
#             "port": 27017,
#             "pool_size": 5,
#             "user_name": "",
#             "password": "",
#             "db_name": "ylcloud"
#         },
#         "mysql": {
#             "type": DB_TYPE["mysql"],
#             "host": "172.16.4.222",
#             "port": 3306,
#             "pool_size": 5,
#             "user_name": "root",
#             "password": "abc123!@#ABC",
#             "db_name": "bosspay"
#         }
#     }
#     db = models._init_db(dbs=dbs)
#     print "done"


# def tmp_get_mysql_test():
#     config = {
#         "type": "mysql",
#         "host": "172.16.4.222",
#         "port": 3306,
#         "pool_size": 0,
#         "user_name": "root",
#         "password": "abc123!@#ABC",
#         "db_name": "bosspay"
#     }
#     with models._get_mysql(config) as obj: ## with db['mysql'] as mysql:
#         cursor = obj.get_cursor()
#         sql = "select * from test"
#         cursor.execute(sql)
#         result = cursor.fetchone()
#         print result
#         time.sleep(10)
#
#
# def tmp_get_mongo_test():
#     config = {
#             "type": "mongodb",
#             "host": "10.10.0.100",
#             "port": 27017,
#             "pool_size": 5,
#             "user_name": "",
#             "password": "",
#             "db_name": "ylcloud"
#         }
#     from framework.db import _get_mongo
    # a = _get_mongo(config)
    # print a.collection_names()
#     import time
#     time.sleep(15)
#
# tmp_get_mongo_test()
# if __name__ == '__main__':
#     pytest.main("test_init_.py::test_init_db")
