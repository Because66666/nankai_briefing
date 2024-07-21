import time
from init import app
import requests
from model import *
from my_logger import logger
import json


def send_group_msg_qq(group_num, title, time_push, url, from_place, type):
    msg = f"【{from_place}·{type}】\n{title}\n发布时间：{time_push}\n链接：{url}"

    data = msg.replace(" ", "%20")
    data = data.replace("\n", "%0a")
    requests.get("http://127.0.0.1:5700/send_group_msg?group_id=" + str(group_num) +
                 "&message=" + data)


def seng_fs_msg(title: str, time_push: str, url: str, from_place: str, type: str, to_who_phone_number: str):
    def refresh_access_token():
        from dotenv import load_dotenv, find_dotenv
        import os
        # load env parameters form file named .env
        load_dotenv(find_dotenv())
        APP_ID = os.getenv("APP_ID")
        APP_SECRET = os.getenv("APP_SECRET")
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": APP_ID,
            "app_secret": APP_SECRET
        }
        response = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                                 headers=headers, json=data)
        ts = int(time.time())+int(response.json()["expire"])
        return response.json()["tenant_access_token"], ts

    def refresh_user_open_id(user_phone: str, user_email: str, access_token: str):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + access_token}
        url = 'https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id'
        if not user_email:
            data = {
                "mobiles": [
                    user_phone
                ]
            }
        else:
            data = {
                "emails": [
                    user_email
                ],
                "mobiles": [
                    user_phone
                ]
            }
        ans = requests.post(url, headers=headers, json=data)
        data1 = ans.json()["data"]['user_list']
        user_open_id = None
        for i in data1:
            if 'user_id' in i:
                user_open_id = i['user_id']
                break
        return user_open_id

    # 首先从数据库中读取access_token以及过期时间token_expires
    # 如果过期了则需要重新申请
    # 其次从用户数据表user_sub中读取user_open_id和user_open_id_ts
    # user_open_id_ts这个是过期时间，如果过期了需要重新查询
    # 查询时需要注意权限是否开放，以及是否有权限查看用户的范围。你可以在开发者后台应用详情页的 权限管理 > 数据权限 > 通讯录权限范围 中，指定用户权限范围。


    # 卡片模板
    ka = {
        "config": {
            "wide_screen_mode": True
        },
        "elements": [
            {
                "tag": "img",
                "img_key": "img_v2_bca29059-d28f-42d4-94a8-fe9078b3d96g",
                "alt": {
                    "tag": "plain_text",
                    "content": ""
                },
                "mode": "fit_horizontal",
                "preview": True
            },
            {
                "tag": "div",
                "text": {
                    "content": f"【{from_place}·{type}】\n{title}\n发布时间：{time_push}",
                    "tag": "lark_md"
                }
            },
            {
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "content": "链接跳转",
                            "tag": "plain_text"
                        },
                        "type": "primary",
                        "multi_url": {
                            "url": f"{url}",
                            "pc_url": "",
                            "android_url": "",
                            "ios_url": ""
                        }
                    }
                ],
                "tag": "action"
            }
        ],
        "header": {
            "template": "turquoise",
            "title": {
                "content": f"{title}",
                "tag": "plain_text"
            }
        },
        "card_link": {
            "url": "",
            "pc_url": "",
            "android_url": "",
            "ios_url": ""
        }
    }

    # 检查access_token是否过期
    find_handle = fs_app_info.query.filter_by(id=1).first()
    if find_handle:
        tenant_access_token = find_handle.tenant_access_token
        token_expires = find_handle.token_expires
        if token_expires < int(time.time()): # access_token过期
            token , ts = refresh_access_token()
            find_handle.token_expires = ts
            find_handle.tenant_access_token = token
            db.session.commit()
        else:
            token = tenant_access_token
    else:
        token, ts = refresh_access_token()
        a = fs_app_info(id=1,token_expires=ts,tenant_access_token=token)
        db.session.add(a)
        db.session.commit()


    # 检查订阅了服务的用户
    find_handle2 = user_sub.query.filter_by(user_phone=to_who_phone_number).first()
    if find_handle2:
        to_who = find_handle2.user_open_id
    else:
        logger.warning(f'用户{to_who_phone_number}未在数据库注册!')
        return
    data = {
        "receive_id": to_who,
        "msg_type": "interactive",
        "content": json.dumps(ka)
    }
    # 注意 access_token具有时效性
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token}
    url = 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id'
    ans = requests.post(url, headers=headers, json=data)
    if ans.status_code != 200:
        code = ans.json()['code']
        logger.warning(f'发送失败,状态码{ans.status_code},错误内容{ans.text}\n再次尝试···')
        if int(code)==99992361:
            user_open_id = refresh_user_open_id(to_who_phone_number,None,token)
            find_handle2.user_open_id = user_open_id
            db.session.commit()
            data = {
                "receive_id": to_who,
                "msg_type": "interactive",
                "content": json.dumps(ka)
            }
            ans2 = requests.post(url, headers=headers, json=data)


#    j = Dean(title=title,time_push=time_push,
#             url=url,push_time = datetime.datetime(int(now[0]),int(now[1]),int(now[2])),
#              from_place='教务处',type='通知公告')
class Send():
    def __init__(self, title: str, time_push: str, url: str, from_place: str, type: str):
        find_handler = user_sub.query.filter_by(sub_place=from_place, sub_type=type).all()
        if find_handler == []:
            return
        for i in find_handler:
            place = i.place
            group = i.group
            if place == 'qq':
                if group != None:
                    send_group_msg_qq(group, title, time_push, url, from_place, type)
                else:
                    logger.warning('group参数为None！！！')
            elif place == 'fs':
                user_phone = i.user_phone
                seng_fs_msg(title, time_push, url, from_place, type, user_phone)
            time.sleep(3)


if __name__ == '__main__':
    user_id = '18707492442'
    title = '测试'
    time_push = 'today'
    url = 'https://www.baidu.com'
    from_place = '教务处'
    type = '通知公告'
    with app.app_context():
        seng_fs_msg(title, time_push, url, from_place, type, user_id)

    pass
