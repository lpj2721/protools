#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/28 9:42
"""
from sqlalchemy.event import listens_for
from sqlalchemy.engine import Engine
from app.conf.config import pool_log_config, sqltime_log_config
from app.untils.log_builder import build_log
import time
pool_logger = build_log(pool_log_config)
sqltime_logger = build_log(sqltime_log_config)


@listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    conn.info.setdefault('query_start_time',time.time())
    sqltime_logger.debug("Start Query: {},Query Parameters: {}".format(statement,parameters))


@listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    total = time.time() - conn.info['query_start_time']
    sqltime_logger.debug("Start Query: {},Query Parameters: {},Query Complete!Total Time:{}".
                         format(statement, parameters, total))


@listens_for(Engine, "connect")
def my_on_connect(dbapi_connection, connection_record):
    print("New DBAPI connection:", dbapi_connection)
    print("Connection record:", connection_record)
    pass

