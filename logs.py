# -*- coding: UTF-8 -*-
import os
import time
import logging

from utility.util_config import get_config_value


# 获取日志文件路径
log_path = get_config_value('LOG_CONF', 'LOG_PATH')


def log_fun(func_name):
    # 获取当天日期
    today = time.localtime()
    today = time.strftime('%Y-%m-%d', today)  # 2019-04-24形式

    # 拼接日志文件
    today_log = '{}-{}-{}'.format(func_name, today, 'log.txt')
    today_log = os.path.join(log_path, today_log)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    # 构建日志对象
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(today_log)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger, handler


def spider_log_info(message):
    logger, handler = log_fun('spider')
    logger.info(message)
    logger.removeHandler(handler)


def web_log_info(message):
    logger, handler = log_fun('web')
    logger.info(message)
    logger.removeHandler(handler)


if __name__ == '__main__':
    spider_log_info('error')
    web_log_info('error')
