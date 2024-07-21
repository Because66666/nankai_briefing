from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_apscheduler import APScheduler
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from flask_migrate import Migrate
from flask_caching import Cache
import requests

# 初始化变量脚本

# 判断系统
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app = Flask('南开简报')
# 实例化程序
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
# 链接、配置数据库的URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 配置缓存类型
app.config['CACHE_TYPE'] = 'filesystem'
# app.config['CACHE_NO_NULL_WARNING']=True



# 创建logger
logger = logging.getLogger('flask')
logger.setLevel(logging.INFO)

# 创建写入日志的handler
file_handler = RotatingFileHandler('./logs/flask.log',maxBytes=10*1024*1024,backupCount=10)
file_handler.setLevel(logging.INFO)

# 创建输出到控制台的handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 设置日志级别

# 定义输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
ch.setFormatter(formatter)

#添加到处理器中
logger.addHandler(file_handler)
logger.addHandler(ch)


db = SQLAlchemy(app)
migrate = Migrate()
migrate.init_app(app, db)
sch = APScheduler()
sch.api_enabled=True
sch.init_app(app)
sch.start()
cache = Cache()
cache.init_app(app,config={'CACHE_TYPE': 'simple'})

allowed={
    'Because':'zsj8320491'
}


