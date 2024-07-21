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
    url = "https://news.nankai.edu.cn/ywsd/index.shtml"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)", "Connection": "close"}
    ans = requests.get(url,headers=headers)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find('td',attrs={'style':"line-height:48px; font-size:16px; background:url(http://news.nankai.edu.cn/ywsd/images/list_08.jpg) 10px 21px repeat-y; padding-left:30px;  "}).contents
    lists = []
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '南开大学新闻网'
            msg['type'] = '南开要闻'
            msg['name'] = re.split('\n',i.text)[2]
            msg['time'] = re.split('\n',i.text)[3]
            msg['url'] = i.contents[1].contents[1].contents[0].contents[0].attrs['href']
            lists.append(msg)
    return lists

def get_data_2()->list:
    url = "https://news.nankai.edu.cn/sp/index.shtml"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)", "Connection": "close"}
    ans = requests.get(url,headers=headers)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find('td',attrs={'style':"line-height:48px; font-size:16px; background:url(http://news.nankai.edu.cn/ywsd/images/list_08.jpg) 10px 21px repeat-y; padding-left:30px;  "}).contents
    lists = []
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '南开大学新闻网'
            msg['type'] = '视频'
            msg['name'] = re.split('\n',i.text)[2]
            msg['time'] = re.split('\n',i.text)[3]
            msg['url'] = i.contents[1].contents[1].contents[0].contents[0].attrs['href']
            lists.append(msg)
    return lists

def get_data_3()->list:
    url = "https://news.nankai.edu.cn/nkdxb/index.shtml"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)", "Connection": "close"}
    ans = requests.get(url,headers=headers)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find('td',attrs={'style':"line-height:48px; font-size:16px; background:url(http://news.nankai.edu.cn/ywsd/images/list_08.jpg) 10px 21px repeat-y; padding-left:30px;  "}).contents
    lists = []
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '南开大学新闻网'
            msg['type'] = '南开大学报'
            msg['name'] = re.split('\n',i.text)[2]
            msg['time'] = re.split('\n',i.text)[3]
            msg['url'] = i.contents[1].contents[1].contents[0].contents[0].attrs['href']
            lists.append(msg)
    return lists


def write_db(msg:dict):
    i = msg
    title = i['name']
    time_push = i['time']
    url = i['url']
    type=i['type']
    from_ =i['from']
    now = re.split('-', time_push)
    j = Dean(title=title,time_push=time_push,
            url=url,push_time = datetime.datetime(int(now[0]),int(now[1]),int(now[2])),
             from_place=from_,type=type)
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
    time.sleep(1.2)
    datas+=get_data_2()
    time.sleep(1.3)
    datas+=get_data_3()

    for j in datas:
        title = j['name']
        if not check_db(title):
            # 不存在的时候
            write_db(j)
            time_push = j['time']
            url = j['url']
            from_place = j['from']
            type = j['type']
            logger.info(f'发现新数据，来自{from_place},{type}')
            Send(title=title,time_push=time_push,url=url,from_place=from_place,type=type)
        else:
            # 存在的时候
            continue



