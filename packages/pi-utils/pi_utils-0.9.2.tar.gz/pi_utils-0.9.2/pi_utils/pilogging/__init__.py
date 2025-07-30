#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Odin <odinmanlee@gmail.com>
#
# Distributed under terms of the MIT license.

"""
log
"""

import sys,logging  # 引入logging模块


class ColoredLevel(logging.Filter):
    """
    Log filter to enable `%(levelname)s` colord
    """

    def filter(self, record):
        """set level color"""
        if record.levelno == logging.DEBUG:
            record.levelname = "\x1b[30;42m" + record.levelname + "\x1b[0m"
        elif record.levelno == logging.INFO:
            record.levelname = "\x1b[30;44m" + record.levelname + "\x1b[0m"
        elif record.levelno == logging.WARNING:
            record.levelname = "\x1b[30;43m" + record.levelname + "\x1b[0m"
        elif record.levelno == logging.ERROR:
            record.levelname = "\x1b[30;41m" + record.levelname + "\x1b[0m"
        elif record.levelno == logging.CRITICAL:
            record.levelname = "\x1b[30;45m" + record.levelname + "\x1b[0m"
        else:
            record.levelname = "\x1b[30;47m" + record.levelname + "\x1b[0m"
        return True


# 创建两个 handler：一个输出到 stdout，另一个输出到 stderr
stdout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)

# 设置 formatter（可复用）
formatter = logging.Formatter(
    "%(asctime)s[%(levelname)s] %(message)s [%(filename)s:%(lineno)d]"
)

# 配置 stdout handler：只处理 DEBUG, INFO 和 WARNING
stdout_handler.setFormatter(formatter)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(lambda record: record.levelno <= logging.WARNING)

# 配置 stderr handler：只处理 ERROR 及以上
stderr_handler.setFormatter(formatter)
stderr_handler.setLevel(logging.ERROR)

# 获取 logger 并添加 handlers
Logger = logging.getLogger()
Logger.setLevel(logging.INFO)  # Log等级总开关
Logger.addFilter(ColoredLevel())
Logger.addHandler(stdout_handler)
Logger.addHandler(stderr_handler)

if __name__ == "__main__":
    Logger.debug("debug message")
    Logger.info("info message")
    Logger.warning("warning message")
    Logger.error("error message")
    Logger.critical("critical message")
