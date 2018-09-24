"""
通用工具类
"""
import datetime
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
