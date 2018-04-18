# _*_ coding:utf-8 _*_
__author__ = "lixiang"
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 本机IP
LOCAL_IP = "192.168.7.1"

# 错误日志
ERROR_LOG_FILE = os.path.join(BASE_DIR, "log", 'error.log')
# 运行日志
RUN_LOG_FILE = os.path.join(BASE_DIR, "log", 'run.log')

# 采集资产的方式，选项有：agent(默认),ssh
MODE = "agent"

# agent模式保存服务器唯一ID的文件
CERT_FILE_PATH = os.path.join(BASE_DIR, "config", "cert")

# 服务器配置
servier = {
    "HostID": 1,
    # 服务器地址
    "Host": "192.168.6.20",
    # 服务器端口
    "Port": 8000,
    # 服务器连接超时时间
    "RequestTimeout": 30,
}

# cmdb配置
cmdb = {

    "cmdb_report": "jasset/api",

    # 每3个小时更新
    "ConfigUpdateInterval": 10800,
}

# 监控
monitor = {
    "urls": {
        # 请求服务api地址
        "get_configs": ["api/monitor/config", 'get'],
        # 返回数据的api地址
        "service_report": ["api/monitor/config/service/report", "post"]
    },
    # 超时时间
    "RequestTimeout": 30,
    # 每5钟更新
    "ConfigUpdateInterval": 300,
}
