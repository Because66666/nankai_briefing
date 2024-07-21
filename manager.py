# 用于数据库全员更新的时候使用的 草稿脚本
from model import *
from init import app
import requests
import time

with app.app_context():
    from model import *
    a = Dean.query.filter(Dean.url.contains('附上源')).all()
    for i in a:
        db.session.delete(i)
        db.session.commit()