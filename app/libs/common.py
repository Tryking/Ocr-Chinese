"""
通用工具类
"""
import datetime
import logging
import os
import time
from logging import handlers


def init_log(console_level, file_level, logfile):
    formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s')
    logging.getLogger().setLevel(0)
    console_log = logging.StreamHandler()
    console_log.setLevel(console_level)
    console_log.setFormatter(formatter)
    file_log = handlers.RotatingFileHandler(logfile, maxBytes=1024 * 1024, backupCount=5)
    file_log.setLevel(file_level)
    file_log.setFormatter(formatter)
    logging.getLogger().addHandler(file_log)
    logging.getLogger().addHandler(console_log)


def get_result_param_value(param, result):
    """
    从请求结果中获取参数值
    :param param:
    :param result:
    :return:
    """
    if param in result:
        return result[param]
    else:
        return None


def get_now():
    ct = time.time()
    local_time = time.localtime(ct)
    date_head = time.strftime("%Y%m%d%H%M%S", local_time)
    date_m_secs = str(datetime.datetime.now().timestamp()).split(".")[-1]
    time_stamp = "%s%.3s" % (date_head, date_m_secs)

    return time_stamp