"""
通用工具类
"""
import datetime
import logging
import os
import time


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


def write_file_log(msg, module='', level='error'):
    filename = os.path.split(__file__)[1]
    if level == 'debug':
        logging.getLogger().debug('File:' + filename + ', ' + module + ': ' + msg)
    elif level == 'warning':
        logging.getLogger().warning('File:' + filename + ', ' + module + ': ' + msg)
    else:
        logging.getLogger().error('File:' + filename + ', ' + module + ': ' + msg)


# debug
def debug(msg, func_name=''):
    module = "%s" % func_name
    write_file_log(msg, module, 'debug')


# error
def error(msg, func_time=''):
    module = "%s" % func_time
    write_file_log(msg, module, 'error')
