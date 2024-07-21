import pprint
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from init import db,sch
from model import Lecture
from api import send_group_msg
from fake_useragent import UserAgent


def login(pages=3):
    user_agent = UserAgent().random
    service = Service('D:\python\爬虫学习\定向消息获取爬虫\edge\msedge.exe geckodriver.exe')
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")
    options.add_argument("--user-agent={}".format(user_agent))
    options.add_experimental_option('useAutomationExtension', False)
    wb = webdriver.Edge(service=service,options=options)
    wb.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    url = r"https://webvpn.nankai.edu.cn/http/77726476706e69737468656265737421f6e25989227e6651700388a5d650272049f668/student/kbmhd/p/1.html"

    wb.get(url)
    wb.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div[2]/ul/li[2]/input').send_keys('2210414')
    wb.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div[2]/ul/li[3]/input').send_keys('Zy75hl73sj04')
    hua=wb.find_element(By.XPATH,'//*[@id="btn"]')
    kuang = wb.find_element(By.XPATH,'//*[@id="slide_box"]')
    ActionChains(wb).drag_and_drop_by_offset(hua,xoffset=kuang.size['width']-hua.size['width'],yoffset=kuang.size['height']).perform()
    wb.find_element(By.XPATH,'//*[@id="submitRole"]').click()
    time.sleep(1.5)
    url2='https://webvpn.nankai.edu.cn/https/77726476706e69737468656265737421e8f043d22931665b7f01c7a99c406d365d/home/user/login.html'
    wb.find_element(By.XPATH,'//*[@id="__layout"]/div/div/div[2]/div/div/div[2]/input').send_keys(url2)
    wb.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[2]/div/div/div[2]/input').send_keys(Keys.ENTER)
    time.sleep(1.5)
    windows = wb.window_handles
    wb.switch_to.window(windows[-1])
    element = WebDriverWait(wb, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="user_login"]/ul/li[1]/a')))  # 等待元素出现
    element.click()
    windows = wb.window_handles
    wb.switch_to.window(windows[-1])
    js = "window.scrollTo(0, document.body.scrollHeight)"
    wb.execute_script(js)  # 模拟鼠标滚轮，滑动页面至底部
    wb.find_element(By.XPATH,'//*[@id="left"]/ul/li[3]/ul/li[1]/a').click()
    htmls=[]
    for i in range(pages):
        # print(wb.current_url[-20:])
        html = wb.page_source
        htmls.append(html)
        js = "window.scrollTo(0, 200)"
        wb.execute_script(js)  # 模拟鼠标滚轮，滑动页面
        time.sleep(3)
        wb.find_element(By.XPATH,'//*[@class="next"]').click()# 下一页
    return htmls

def any(html):
    h = BeautifulSoup(html, 'lxml')
    lists = h.find_all('tr')
    lists = lists[2:]
    data_base = list()
    for i in lists:
        li_2 = i.find_all('td')
        data_one = {
            'title': li_2[0].text,
            'type': li_2[1].text,
            'time_set': li_2[2].text,
            'time_begin': li_2[3].text,
            'place': li_2[4].text,
            'url': 'https://webvpn.nankai.edu.cn' + li_2[5].contents[1].attrs['href']
        }
        data_base.append(data_one)
    return data_base

def write_db(msg:dict):
    i = msg
    title = i['title']
    type = i['type']
    time_set = i['time_set']
    time_begin = i['time_begin']
    place = i['place']
    url = i['url']
    j = Lecture(title=title,type=type,time_set=time_set,
                  time_begin=time_begin,place=place,
                  url=url)
    db.session.add(j)
    db.session.commit()

def check_db(title:str):
    lecture = Lecture.query.filter_by(title = title).first()
    if lecture == None:
        # 不存在的时候返回False
        return False
    # 存在的时候返回True
    else:
        return True

def check_db_none():
    lecture = Lecture.query.all()
    if len(lecture) ==0:
        # 是否为第一次
        return True
    else:
        # 不是第一次
        return False



def run():
    aaa = check_db_none()
    htmls=login()
    for i in htmls:
        a = any(i)
        for j in a:
            title = j['title']
            if not check_db(title):
                # 不存在的时候
                write_db(j)
                if not aaa:
                    msg = "【主题讲座】\n"
                    msg += j['title']+'\n'
                    msg += '学时：'+ j['time_set'] + '\n'
                    msg += '时间：'+j['time_begin']+'\n'
                    msg+='地点：'+j['place']+'\n'
                    msg+='链接：'+j['url']
                    send_group_msg(msg,773879783)
                time.sleep(60)
            else:
                # 存在的时候
                continue


htmls = login()
pprint.pp(htmls)

