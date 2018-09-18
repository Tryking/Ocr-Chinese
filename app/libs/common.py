"""
通用工具类
"""


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
