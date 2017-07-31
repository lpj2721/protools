#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/28 10:37
"""
import logging as log
import sys
from logging.handlers import SysLogHandler
from logging.handlers import TimedRotatingFileHandler


level_dic = {
    "debug": log.DEBUG,
    "info": log.INFO,
    "waring": log.WARNING,
    "error": log.ERROR,
    "fatal": log.FATAL
}


def get_level(level_str):
    return level_dic[level_str.lower()]


def build_log(log_config):
    logging = log.getLogger(log_config['name'])
    level = get_level(log_config['level'])
    formatter = log.Formatter(log_config['format'])
    logging.setLevel(level)
    if log_config['file']['enable']:
        __file_handler = TimedRotatingFileHandler(log_config['file']['path'], when="D")
        __file_handler.setFormatter(formatter)
        logging.addHandler(__file_handler)
    if log_config['console']:
        __console_handler = log.StreamHandler(stream=sys.stdout, )
        __console_handler.setFormatter(formatter)
        logging.addHandler(__console_handler)
    if log_config['syslog']['enable']:
        __syslog_handler = SysLogHandler(address=(log_config['syslog']['ip'], log_config['syslog']['port']),
                                         facility=log_config['syslog']['facility'])
        __syslog_handler.setFormatter(formatter)
        logging.addHandler(__syslog_handler)
    return logging