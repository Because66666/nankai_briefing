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
s.headers=headers

def get_data()->list:
    url = "https://cyber.nankai.edu.cn/"
    ans = s.get(url)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    lists = []

    a = text.find('div', attrs={'id': 'wp_news_w20'}).contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '网络空间安全学院'
            msg['type'] = '学院公告'
            msg['name'] = i.find('span').text
            msg['time'] = i.find_all('span')[2].text
            msg['url'] = 'https://cyber.nankai.edu.cn/'+i.attrs['href']
            lists.append(msg)

    a = text.find('div', attrs={'id': 'wp_news_w5'}).contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '网络空间安全学院'
            msg['type'] = '最新动态'
            msg['name'] = i.find('span').text
            msg['time'] = i.find_all('span')[2].text
            msg['url'] = 'https://cyber.nankai.edu.cn/'+i.attrs['href']
            lists.append(msg)

    a = text.find('div', attrs={'id': 'wp_news_w21'}).contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '网络空间安全学院'
            msg['type'] = '学生工作通知'
            msg['name'] = i.find('span').text
            msg['time'] = i.find_all('span')[2].text
            msg['url'] = 'https://cyber.nankai.edu.cn/'+i.attrs['href']
            lists.append(msg)

    a = text.find('div', attrs={'id': 'wp_news_w22'}).contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '网络空间安全学院'
            msg['type'] = '科研信息'
            msg['name'] = i.find('span').text
            msg['time'] = i.find_all('span')[2].text
            msg['url'] = 'https://cyber.nankai.edu.cn/'+i.attrs['href']
            lists.append(msg)

    a = text.find('div', attrs={'id': 'wp_news_w23'}).contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '网络空间安全学院'
            msg['type'] = '本科生教学'
            msg['name'] = i.find('span').text
            msg['time'] = i.find_all('span')[2].text
            msg['url'] = 'https://cyber.nankai.edu.cn/'+i.attrs['href']
            lists.append(msg)

    a = text.find('div', attrs={'id': 'wp_news_w24'}).contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '网络空间安全学院'
            msg['type'] = '研究生招生'
            msg['name'] = i.find('span').text
            msg['time'] = i.find_all('span')[2].text
            msg['url'] = 'https://cyber.nankai.edu.cn/' + i.attrs['href']
            lists.append(msg)

    a = text.find('div', attrs={'id': 'wp_news_w26'}).contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '网络空间安全学院'
            msg['type'] = '党团园地'
            msg['name'] = i.find('span').text
            msg['time'] = i.find_all('span')[2].text
            msg['url'] = 'https://cyber.nankai.edu.cn/' + i.attrs['href']
            lists.append(msg)

    a = text.find('div', attrs={'id': 'wp_news_w27'}).contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '网络空间安全学院'
            msg['type'] = '就业信息'
            msg['name'] = i.find('span').text
            msg['time'] = i.find_all('span')[2].text
            msg['url'] = 'https://cyber.nankai.edu.cn/' + i.attrs['href']
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
    time.sleep(1.3)


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

if __name__ == '__main__':
    datas = get_data()
    print(datas)

