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
    url = "https://wxy.nankai.edu.cn/"
    ans = s.get(url)
    html = ans.content.decode()
    text = BeautifulSoup(html, features='lxml')  # 解析库分析
    lists = []

    a = text.find('div', attrs={'id': 'wp_news_w12'}).find('ul').contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '文学院'
            msg['type'] = '新闻动态'
            msg['name'] = i.find('a').text
            msg['time'] = str(i.find('div').find('div',attrs={'class':'news_days'}).text+'-'+
                           i.find('div').find('div',attrs={'class':'news_year'}).text)
            msg['url'] = url+i.find('a').attrs['href']
            lists.append(msg)

    a = text.find('div', attrs={'id': 'wp_news_w20'}).find('ul').contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '文学院'
            msg['type'] = '通知公告'
            msg['name'] = i.find('a').text
            msg['time'] = str(i.find('div').find('div',attrs={'class':'news_days'}).text+'-'+
                           i.find('div').find('div',attrs={'class':'news_year'}).text)
            msg['url'] = url+i.find('a').attrs['href']
            lists.append(msg)

    a = text.find('div', attrs={'id': 'wp_news_w21'}).find('ul').contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '文学院'
            msg['type'] = '讲座信息'
            msg['name'] = i.find('a').text
            msg['time'] = str(i.find('div').find('div',attrs={'class':'news_days'}).text+'-'+
                           i.find('div').find('div',attrs={'class':'news_year'}).text)
            msg['url'] = url+i.find('a').attrs['href']
            lists.append(msg)

    a = text.find('div', attrs={'id': 'wp_news_w22'}).find('ul').contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '文学院'
            msg['type'] = '学术研究'
            msg['name'] = i.find('a').text
            msg['time'] = str(i.find('div').find('div', attrs={'class': 'news_days'}).text + '-' +
                              i.find('div').find('div', attrs={'class': 'news_year'}).text)
            msg['url'] = url + i.find('a').attrs['href']
            lists.append(msg)

    time.sleep(1.1)
    ans1 = s.get('https://wxy.nankai.edu.cn/bkjy/list.htm')
    html1 = ans1.content.decode()
    text1 = BeautifulSoup(html1, features='lxml')  # 解析库分析
    a = text1.find('div', attrs={'id': 'wp_news_w6'}).find('ul').contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '文学院'
            msg['type'] = '本科教育-活动信息'
            msg['name'] = i.find('a').text
            msg['time'] = i.find('span',attrs={'class':'news_meta'}).text
            msg['url'] = url + i.find('a').attrs['href']
            lists.append(msg)

    time.sleep(1.1)
    ans1 = s.get('https://wxy.nankai.edu.cn/kcap/list.htm')
    html1 = ans1.content.decode()
    text1 = BeautifulSoup(html1, features='lxml')  # 解析库分析
    a = text1.find('div', attrs={'id': 'wp_news_w6'}).find('ul').contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '文学院'
            msg['type'] = '本科教育-课程安排'
            msg['name'] = i.find('a').text
            msg['time'] = i.find('span',attrs={'class':'news_meta'}).text
            msg['url'] = url + i.find('a').attrs['href']
            lists.append(msg)

    time.sleep(1.1)
    ans1 = s.get('https://wxy.nankai.edu.cn/p32582c15652/list.htm')
    html1 = ans1.content.decode()
    text1 = BeautifulSoup(html1, features='lxml')  # 解析库分析
    a = text1.find('div', attrs={'id': 'wp_news_w6'}).find('ul').contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '文学院'
            msg['type'] = '媒体聚焦'
            msg['name'] = i.find('a').text
            msg['time'] = i.find('span',attrs={'class':'news_meta'}).text
            url_0 = i.find('a').attrs['href']
            if 'https:' in url_0:
                msg['url'] = url_0
            else:
                msg['url'] = url + url_0
            lists.append(msg)

    time.sleep(1.1)
    ans1 = s.get('https://wxy.nankai.edu.cn/xsqk/list.htm')
    html1 = ans1.content.decode()
    text1 = BeautifulSoup(html1, features='lxml')  # 解析库分析
    a = text1.find('div', attrs={'id': 'wp_news_w6'}).find('ul').contents
    for i in a:
        if len(i) != 1:
            msg = {}
            msg['from'] = '文学院'
            msg['type'] = '学术期刊《南开语言学刊》'
            msg['name'] = i.find('a').text
            msg['time'] = i.find('span',attrs={'class':'news_meta'}).text
            msg['url'] = url + i.find('a').attrs['href']
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

