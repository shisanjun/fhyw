# _*_ coding:utf-8 _*_
__author__ = "lixiang"

import os
import logging

from conf import settings

class Logger(object):
    __instance=None
    def __init__(self):
        self.run_log_file=settings.RUN_LOG_FILE
        self.error_log_file=settings.ERROR_LOG_FILE
        self.run_logger=None
        self.error_logger=None

        self.init_error_log()
        self.init_run_log()

    def __new__(cls, *args, **kwargs):
        """单例模式只返回一个实例"""
        if not cls.__instance:
            cls.__instance=object.__new__(cls,*args,**kwargs)
        return cls.__instance

    @staticmethod
    def _check_path_exist(abs_log_file):
        """判断文件目录是否存在，不存在则创建"""
        log_path=os.path.split(abs_log_file)[0]
        if not os.path.exists(log_path):
            os.mkdir(log_path)

    def init_run_log(self):
        """初始化run log handle"""
        self._check_path_exist(self.run_log_file)
        file_log=logging.FileHandler(self.run_log_file,'a',encoding="utf-8")
        fmt=logging.Formatter(fmt="%(asctime)s - %(levelname)s : %(message)s")
        file_log.setFormatter(fmt)
        logger1=logging.Logger("run_log",level=logging.INFO)
        logger1.addHandler(file_log)
        self.run_logger=logger1

    def init_error_log(self):
        """初始化error log handle"""
        self._check_path_exist(self.error_log_file)
        file_log=logging.FileHandler(self.error_log_file,'a',encoding="utf-8")
        fmt=logging.Formatter(fmt="%(asctime)s - %(levelname)s : %(message)s")
        file_log.setFormatter(fmt)
        logger1=logging.Logger("error_log",level=logging.INFO)
        logger1.addHandler(file_log)
        self.error_logger=logger1

    def log(self,message,mode=True):
        """
        写入日志
        :param message:日志信息
        :param mode:True表示运行日志，False表示错误信息
        :return:
        """
        if mode:
            self.run_logger.info(message)
        else:
            self.error_logger.info(message)