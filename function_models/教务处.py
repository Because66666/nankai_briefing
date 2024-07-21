import datetime
import sys
sys.path.append("..")
from model import Dean
import time
import requests
from bs4 import BeautifulSoup
import re
from init import db,logger
from manager_of_sending import Send


def get_data()->list:
    url = "http://jwc.nankai.edu.cn/24/list.htm"# 网页地址
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"
    } # 请求头设置
    ans = requests.get(url,headers=headers) # 发送请求，返回值为服务器响应
    html = ans.content.decode() # 将二进制转码为utf-8
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find(attrs={'class': 'wp_article_list'}).contents
    # 元素列表在class属性为wp_article_list的元素下面
    lists = []
    for i in a:
        if len(i) == 5:
            msg = {}
            msg['from'] = '南开大学教务处'
            msg['type'] = '通知公告'
            msg['name'] = re.split('\n', i.text)[3]
            msg['time'] = re.split('\n', i.text)[-3]
            msg['url'] = "http://jwc.nankai.edu.cn"+i.contents[1].find_all('span')[1].contents[0].attrs['href']
            lists.append(msg)
    return lists

def get_data_2()->list:
    url = "http://jwc.nankai.edu.cn/20/list.htm"# 网页地址
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"
    } # 请求头设置
    ans = requests.get(url,headers=headers) # 发送请求，返回值为服务器响应
    html = ans.content.decode() # 将二进制转码为utf-8
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find(attrs={'class': 'wp_article_list'}).contents
    # 元素列表在class属性为wp_article_list的元素下面
    lists = []
    for i in a:
        if len(i) == 5:
            msg = {}
            msg['from'] = '南开大学教务处'
            msg['type'] = '新闻动态'
            msg['name'] = re.split('\n', i.text)[3]
            msg['time'] = re.split('\n', i.text)[-3]
            msg['url'] = "http://jwc.nankai.edu.cn"+i.contents[1].find_all('span')[1].contents[0].attrs['href']
            lists.append(msg)
    return lists


def write_db(msg:dict):
    i = msg
    title = i['name']
    time_push = i['time']
    url = i['url']
    type = i['type']
    now = re.split('-', time_push)
    j = Dean(title=title,time_push=time_push,
            url=url,push_time = datetime.datetime(int(now[0]),int(now[1]),int(now[2])),
             from_place='教务处',type=type)
    db.session.add(j)
    db.session.commit()


def check_db(title:str):
    dean = Dean.query.filter_by(title = title).first()
    if dean == None:
        # 不存在的时候返回False
        return False
    # 存在的时候返回True
    else:
        return True


def run():
    datas=get_data()
    time.sleep(1)
    datas_2 = get_data_2()
    datas=datas+datas_2
    for j in datas:
        title = j['name']
        if not check_db(title):
            # 不存在的时候
            write_db(j)
            time_push = j['time']
            url = j['url']
            from_place = '教务处'
            type = j['type']
            logger.info(f'发现新数据，来自{from_place},{type}')
            Send(title=title,time_push=time_push,url=url,from_place=from_place,type=type)
        else:
            # 存在的时候
            continue



