import logging
from logging.handlers import RotatingFileHandler
import os

if not os.path.exists('./logs'):
    os.mkdir('./logs')


logger = logging.getLogger('爬虫与推送')
logger.setLevel(logging.INFO)


logger_file = RotatingFileHandler('./logs/log.txt',maxBytes=1*1024*1024,backupCount=10)
logger_file.setLevel(logging.INFO)

# 创建输出到控制台的handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 设置日志级别

# 定义输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_file.setFormatter(formatter)
ch.setFormatter(formatter)

#添加到处理器中
logger.addHandler(logger_file)
logger.addHandler(ch)