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


s = requests.Session()
def get_data()->list:
    url = "https://math.nankai.edu.cn/5536/list.htm"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)", "Connection": "close"}
    ans = s.get(url,headers=headers)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find(attrs={'id': 'wp_news_w6'}).contents[1].contents
    lists = []
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '数学科学学院'
            msg['type'] = '本科生教育'
            msg['name'] = i.contents[0].contents[0]
            msg['time'] = i.contents[1].text
            msg['url'] = "https://math.nankai.edu.cn/"+i.contents[0].attrs['href']
            lists.append(msg)
    return lists

def get_data_2()->list:
    url = "https://math.nankai.edu.cn/5535/list.htm"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)", "Connection": "close"}
    ans = s.get(url,headers=headers)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find(attrs={'id': 'wp_news_w6'}).contents[1].contents
    lists = []
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '数学科学学院'
            msg['type'] = '学院工作'
            msg['name'] = i.contents[0].contents[0]
            msg['time'] = i.contents[1].text
            msg['url'] = "https://math.nankai.edu.cn/"+i.contents[0].attrs['href']
            lists.append(msg)
    return lists

def get_data_3()->list:
    url = "https://math.nankai.edu.cn/5537/list.htm"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)", "Connection": "close"}
    ans = s.get(url,headers=headers)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find(attrs={'id': 'wp_news_w6'}).contents[1].contents
    lists = []
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '数学科学学院'
            msg['type'] = '研究生教育'
            msg['name'] = i.find('a',attrs={'target':'_blank'}).text
            msg['time'] = i.contents[1].text
            msg['url'] = "https://math.nankai.edu.cn/"+i.contents[0].attrs['href']
            lists.append(msg)
    return lists

def get_data_4()->list:
    url = "https://math.nankai.edu.cn/5538/list.htm"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)", "Connection": "close"}
    ans = s.get(url,headers=headers)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find(attrs={'id': 'wp_news_w6'}).contents[1].contents
    lists = []
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '数学科学学院'
            msg['type'] = '科研动态'
            msg['name'] = i.contents[0].contents[0]
            msg['time'] = i.contents[1].text
            msg['url'] = "https://math.nankai.edu.cn/"+i.contents[0].attrs['href']
            lists.append(msg)
    return lists

def get_data_5()->list:
    url = "https://math.nankai.edu.cn/5540/list1.htm"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)", "Connection": "close"}
    ans = s.get(url,headers=headers)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find(attrs={'id': 'wp_news_w6'}).contents[1].contents
    lists = []
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '数学科学学院'
            msg['type'] = '学生工作'
            msg['name'] = i.contents[0].contents[0]
            msg['time'] = i.contents[1].text
            msg['url'] = "https://math.nankai.edu.cn/"+i.contents[0].attrs['href']
            lists.append(msg)
    return lists


def write_db(msg:dict):
    i = msg
    title = i['name']
    time_push = i['time']
    url = i['url']
    type=i['type']
    now = re.split('-', time_push)
    j = Dean(title=title,time_push=time_push,
            url=url,push_time = datetime.datetime(int(now[0]),int(now[1]),int(now[2])),
             from_place='数学科学学院',type=type)
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
    time.sleep(1.1)
    datas+=get_data_2()
    time.sleep(1.2)
    datas+=get_data_3()
    time.sleep(1.3)
    datas+=get_data_4()
    time.sleep(1.4)
    datas+=get_data_5()
    for j in datas:
        title = j['name']
        if not check_db(title):
            # 不存在的时候
            write_db(j)
            time_push = j['time']
            url = j['url']
            from_place = '数学科学学院'
            type = j['type']
            logger.info(f'发现新数据，来自{from_place},{type}')
            Send(title=title,time_push=time_push,url=url,from_place=from_place,type=type)
        else:
            # 存在的时候
            continue



