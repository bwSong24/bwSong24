# -*- coding: utf-8-*-
import datetime
import os
import logging
from logging.handlers import RotatingFileHandler


def config_logging(log_name, file_log_level=logging.DEBUG, stream_log_level=logging.DEBUG, file_size=500, backup_count=20, is_console_output=True):
    pos = log_name.rfind('/')
    log_dir = log_name[:pos]
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 将日志进行分卷
    rt_file_handler = RotatingFileHandler(log_name, mode='a', maxBytes=file_size * 1024 * 1024, backupCount=backup_count)
    rt_file_handler.setLevel(file_log_level)
    formatter = logging.Formatter(
        '%(asctime)s %(process)d:%(thread)d %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    rt_file_handler.setFormatter(formatter)
    logger.addHandler(rt_file_handler)

    # 将日志从控制台输出
    if is_console_output:
        console = logging.StreamHandler()
        console.setLevel(stream_log_level)
        formatter = logging.Formatter(
            '%(asctime)s %(process)d:%(thread)d %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        console.setFormatter(formatter)
        logger.addHandler(console)
        logging.info("cfb_day_hot_recommend run begin at %s" % datetime.datetime.now())

