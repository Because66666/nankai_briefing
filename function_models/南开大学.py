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
headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 HBPC/12.1.3.303',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

def get_data()->list:
    url = "https://www.nankai.edu.cn/157/list.htm"
    ans = s.get(url)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find('ul', attrs={'class': 'newslist'}).contents
    lists = []
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '南开大学'
            msg['type'] = '通知公告'
            msg['name'] = i.contents[3].text
            msg['time'] = re.split('\n',i.contents[1].text)[2].replace(' ','').replace('\t','')+'-'+re.split('\n',i.contents[1].text)[1].replace('\r','')
            msg['url'] = 'https://www.nankai.edu.cn/'+i.contents[3].contents[0].attrs['href']
            lists.append(msg)
    return lists


def get_data_2()->list:
    url = "https://www.nankai.edu.cn/159/list.htm"
    ans = s.get(url)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find('ul', attrs={'class': 'newslist'}).contents
    lists = []
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '南开大学'
            msg['type'] = '校情通报'
            msg['name'] = i.contents[3].text
            msg['time'] = re.split('\n',i.contents[1].text)[2].replace(' ','').replace('\t','')+'-'+re.split('\n',i.contents[1].text)[1].replace('\r','')
            msg['url'] = 'https://www.nankai.edu.cn/'+i.contents[3].contents[0].attrs['href']
            lists.append(msg)
    return lists

def get_data_3()->list:
    url = "https://www.nankai.edu.cn/xshd/list.htm"
    ans = s.get(url)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    a = text.find('ul', attrs={'class': 'newslist'}).contents
    lists = []
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '南开大学'
            msg['type'] = '学术活动'
            msg['name'] = i.contents[3].text
            msg['time'] = re.split('\n',i.contents[1].text)[2].replace(' ','').replace('\t','')+'-'+re.split('\n',i.contents[1].text)[1].replace('\r','')
            msg['url'] = '无链接，附上源：'+'https://www.nankai.edu.cn/xshd/list.htm'
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



