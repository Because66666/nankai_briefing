#!/usr/bin/env python3.9
from api import MessageApiClient
from event import MessageReceiveEvent, UrlVerificationEvent, EventManager, MessageReadEvent
from dotenv import load_dotenv, find_dotenv
import json
from my_logger import *
from init import *
import scheduler
import subprocess
import click
from model import *

from flask import render_template, make_response, jsonify, send_file, request, abort, redirect
from waitress import serve

# flask指令添加
@app.cli.command()
def s():
    db.drop_all()
    click.echo('已删除数据库和表')
    db.create_all()
    click.echo('已重建数据库和表')


@app.cli.command()
def init():
    db.init_app(app)
    click.echo('已初始化数据表')


@app.cli.command()
def u():
    p1 = subprocess.Popen('flask --app server db migrate -m "Initial migration."', shell=True)
    p1.wait()
    p2 = subprocess.Popen('flask --app server db upgrade', shell=True)
    p2.wait()
    click.echo('已更新数据表')


# 注册shell上下文处理函数
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Lecture=Lecture, Dean=Dean, user_sub=user_sub)


# load env parameters form file named .env
load_dotenv(find_dotenv())

ssl_keys = ('cert/ca.crt', 'cert/server.key')
# load from env
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")
ENCRYPT_KEY = ''
LARK_HOST = os.getenv("LARK_HOST")
# init service
message_api_client = MessageApiClient(APP_ID, APP_SECRET, LARK_HOST)
event_manager = EventManager()

# 卡片模板
with app.app_context():
    a1 = Dean.query.all()
    a2 = {i.from_place for i in a1}
    lists = list(a2)
    new_ = [{'text': i, 'value': 'sub:' + i + '-1'} for i in lists]
    ka_pian2 = {
        "config": {
            "enable_forward": True,
            "update_multi": True
        },
        "type": "template",
        "data": {
            "template_id": "ctp_AA8K4uNdyUpV",
            "template_variable":
                {
                    "from_place": new_,
                    "type": [
                        {
                            "text": "请先选择上面一项",
                            "value": "None-2"
                        }
                    ],
                    "state": "请选择",
                    "select_1": "请选择",
                    "select_2": "先选择上面的选项"
                }
        }
    }
    app.config['ka_pian2'] = ka_pian2



@event_manager.register("url_verification")
def request_url_verify_handler(req_data: UrlVerificationEvent):
    # url verification, just need return challenge
    if req_data.event.token != VERIFICATION_TOKEN:
        raise Exception("VERIFICATION_TOKEN is invalid")
    return jsonify({"challenge": req_data.event.challenge})


# 收到消息
@event_manager.register("im.message.receive_v1")
def message_receive_event_handler(req_data: MessageReceiveEvent):
    sender_id = req_data.event.sender.sender_id
    message = req_data.event.message
    if message.message_type != "text":
        logger.warn("Other types of messages have not been processed yet")
        return jsonify()
        # get open_id and text_content
    open_id = sender_id.open_id

    class Command_block():
        def __init__(self):
            self.command_list = {'介绍': '用一段话来介绍自己',
                                 '网页': '提供跳转网页端链接',
                                 '菜单': '今天吃什么？',
                                 '订阅': '如果你想得到推送的话',
                                 '编辑': '订阅太多了太吵了？选这个来编辑订阅'}

        def command(self, msg: str):
            text_content = dict()
            if msg == '菜单':
                a = '可支持的指令如下：\n'
                num = 1
                for i, j in self.command_list.items():
                    a += str(num) + f".{i}\n"
                    num += 1
                a = a[:-1]
                text_content['text'] = a
                text_content2 = json.dumps(text_content)
                type = 'text'

            elif msg == '介绍':
                type = 'text'
                text_content['text'] = '一个由南开大学大一学生自主研发的飞书机器人，目前已经上线服务器，后续功能正在陆续开发中'
                text_content2 = json.dumps(text_content)
            elif msg == '网页':
                ka_pian = {"type": "template", "data": {"template_id": "ctp_AA8KxHaXCxKR",
                                                        "template_variable": {"article_title": "南开简报"}}}
                text_content2 = json.dumps(ka_pian)
                type = 'interactive'
            elif msg == '订阅':
                ka_pian2 = {
        "config": {
            "enable_forward": True,
            "update_multi": True
        },
        "type": "template",
        "data": {
            "template_id": "ctp_AA8K4uNdyUpV",
            "template_variable":
                {
                    "from_place": new_,
                    "type": [
                        {
                            "text": "请先选择上面一项",
                            "value": "None-2"
                        }
                    ],
                    "state": "请选择",
                    "select_1": "请选择",
                    "select_2": "先选择上面的选项"
                }
        }
    }
                text_content2 = json.dumps(ka_pian2)
                type = 'interactive'
            elif msg == '编辑':
                ka_pian13 = {
        "config": {
            "enable_forward": True,
            "update_multi": True
        },
        "elements": [
            {
                "tag": "markdown",
                "content": "**你已订阅的栏目有：**\n${lists}",
                "text_align": "left"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "选择器：请选择要删除哪一个？"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "select_static",
                        "placeholder": {
                            "tag": "plain_text",
                            "content": "${from_1}"
                        },
                        "options": []
                    }
                ]
            },
            {
                "tag": "div",
                "text": {
                    "content": "删除一次后可以再次选择，继续删除；\n当你完成之后点击下方的按钮。",
                    "tag": "plain_text"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "我已完成"
                        },
                        "type": "primary",
                        "value": {
                            "done": "done"
                        }
                    }
                ]
            }
        ],
        "header": {
            "template": "blue",
            "title": {
                "content": "南开简报-订阅编辑",
                "tag": "plain_text"
            }
        }
    }
                find_handle = user_sub.query.filter_by(user_open_id=open_id, place='fs').all()
                if  find_handle == []:
                    ka_pian13['elements'] = [
                        {'tag': 'markdown', 'content': '**噢，你貌似没有订阅？**', 'text_align': 'left'}]
                    text_content2 = json.dumps(ka_pian13)
                    type = 'interactive'
                    message_api_client.send('open_id', open_id, type, text_content2)
                    return
                else:
                    m = str()
                    num = 1
                    for i in find_handle:
                        m += f'{num}.{i.sub_place}-{i.sub_type}\n'
                        num += 1
                        ka_pian13['elements'][2]['actions'][0]['options'].append({'text': {
                            "tag": "plain_text",
                            "content": f"{i.sub_place}-{i.sub_type}"}, 'value': 'del:' + f"{i.sub_place}-{i.sub_type}"}
                         )
                    ka_pian13['elements'][0]['content'] = ka_pian13['elements'][0]['content'].replace('${lists}', m)
                    ka_pian13['elements'][2]['actions'][0]['placeholder']['content'] = \
                    ka_pian13['elements'][2]['actions'][0]['placeholder']['content'].replace('${from_1}', '请选择')

                type = 'interactive'
                text_content2 = json.dumps(ka_pian13)
            else:
                return None

            # message.content:::'{'text':'sjadsad'}',__type__=str
            # print(text_content)
            # print(type(message.content))
            # echo text message
            message_api_client.send('open_id', open_id, type, text_content2)
            return 'OK'

    command_block = Command_block()
    # 调用命令
    with app.app_context():
        text = command_block.command(json.loads(message.content)['text'])
    return jsonify()


# 对方消息已读
@event_manager.register("im.message.message_read_v1")
def message_receive_event_handler2(req_data: MessageReadEvent):
    return jsonify()


@app.errorhandler
def msg_error_handler(ex):
    logging.error(ex)
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.response.status_code if isinstance(ex, requests.HTTPError) else 500
    )
    return response


def ka_pian_handle(msg: dict, open_id: str):
    if msg['tag'] == 'select_static':
        import re
        f_2 = re.split(':', msg['option'])
        if f_2[0] == 'sub':
            from_place_t = re.split('-', f_2[1])
            if from_place_t[1] == '1':
                from_place = from_place_t[0]
                a1 = Dean.query.filter_by(from_place=from_place).all()
                a2 = {i.type for i in a1}
                lists2 = list(a2)
                new2 = [{'text': i, 'value': 'sub:' + i + '-2,' + from_place} for i in lists2]
                ka22 = app.config['ka_pian2']
                ka22['data']['template_variable']['type'] = new2
                ka22['data']['template_variable']['state'] = '完成1/2'
                ka22['data']['template_variable']['select_1'] = "已选择：" + from_place
                ka22['data']['template_variable']['select_2'] = "选择："
                # message_api_client.update(open_message_id, json.dumps(ka22))
                return ka22
            elif '2,' in from_place_t[1]:
                from_place = from_place_t[1].replace('2,', '')
                type = from_place_t[0]
                finder = user_sub.query.filter_by(user_open_id=open_id, sub_place=from_place, sub_type=type,place='fs').first()
                if finder is not None:
                    ka12 = app.config['ka_pian2']
                    ka12['data']['template_variable']['state'] = '已经订阅过了。'
                    return ka12
                sub = user_sub(place='fs', sub_place=from_place, sub_type=type,
                               user_open_id=open_id, user_phone=None, user_email=None)
                db.session.add(sub)
                db.session.commit()
                ka11 = app.config['ka_pian2']
                ka11['data']['template_variable']['state'] = '完成2/2；提交成功；重新选择第一选项可继续添加。'
                ka11['data']['template_variable']['select_1'] = "已选择：" + from_place
                ka11['data']['template_variable']['select_2'] = "已选择：" + type
                return ka11
        elif f_2[0] == 'del':
            from_place_t = re.split('-', f_2[1])
            from_place = from_place_t[0]
            type = from_place_t[1]
            finder = user_sub.query.filter_by(place='fs', user_open_id=open_id, sub_place=from_place,
                                              sub_type=type).first()
            db.session.delete(finder)
            db.session.commit()
            del_finish = from_place + '-' + type
            find_handle = user_sub.query.filter_by(user_open_id=open_id, place='fs').all()
            ka_pian23 = {
        "config": {
            "enable_forward": True,
            "update_multi": True
        },
        "elements": [
            {
                "tag": "markdown",
                "content": "**你已订阅的栏目有：**\n${lists}",
                "text_align": "left"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "选择器：请选择要删除哪一个？"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "select_static",
                        "placeholder": {
                            "tag": "plain_text",
                            "content": "${from_1}"
                        },
                        "options": "${from}"
                    }
                ]
            },
            {
                "tag": "div",
                "text": {
                    "content": "删除一次后可以再次选择，继续删除；\n当你完成之后点击下方的按钮。",
                    "tag": "plain_text"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "我已完成"
                        },
                        "type": "primary",
                        "value": {
                            "done": "done"
                        }
                    }
                ]
            }
        ],
        "header": {
            "template": "blue",
            "title": {
                "content": "南开简报-订阅编辑",
                "tag": "plain_text"
            }
        }
    }
            if find_handle == []:
                ka_pian23['elements'] = [
                    {'tag': 'markdown', 'content': '**刚刚完成删除...噢，你貌似没有订阅？**', 'text_align': 'left'}]
            else:
                m = str()
                num = 1
                for i in find_handle:
                    m += f'{num}.{i.sub_place}-{i.sub_type}\n'
                    num += 1
                ka_pian23['elements'][0]['content'] = ka_pian23['elements'][0]['content'].replace('${lists}', m)
                ka_pian23['elements'][2]['actions'][0]['placeholder']['content'] = \
                ka_pian23['elements'][2]['actions'][0]['placeholder']['content'].replace('${from_1}',
                                                                                        f'已经删除：{del_finish}')
                ka_pian23['elements'][2]['actions'][0]['options'] = [{'text': {
                    "tag": "plain_text",
                    "content": f"{i.sub_place}-{i.sub_type}"}, 'value': 'del:' + f"{i.sub_place}-{i.sub_type}"}
                    for i in find_handle]
            return ka_pian23
    elif msg['tag'] == 'button':
        if msg['value']['done'] =='done':
            ka_pian14 = {
            "config": {
                "enable_forward": True,
                "update_multi": True
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": "**你已订阅的栏目有：**\n${lists}",
                    "text_align": "left"
                },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "继续订阅"
                        },
                        "type": "primary",
                        "value": {
                            "done": "add_sub"
                        }
                    }
                ]
            }
            ],
            "header": {
                "template": "blue",
                "title": {
                    "content": "南开简报-订阅编辑",
                    "tag": "plain_text"
                }
            }
        }
            find_handle = user_sub.query.filter_by(user_open_id=open_id, place='fs').all()
            if find_handle == []:
                ka_pian14['elements'] = [
                    {'tag': 'markdown', 'content': '**刚刚完成删除...\n噢，你貌似没有订阅？**', 'text_align': 'left'}]
            else:
                m = str()
                num = 1
                for i in find_handle:
                    m += f'{num}.{i.sub_place}-{i.sub_type}\n'
                    num += 1
                ka_pian14['elements'][0]['content'] = ka_pian14['elements'][0]['content'].replace('${lists}', m)
            return ka_pian14
        elif msg['value']['done'] =='add_sub':
            ka_pian2 = {
                "config": {
                    "enable_forward": True,
                    "update_multi": True
                },
                "type": "template",
                "data": {
                    "template_id": "ctp_AA8K4uNdyUpV",
                    "template_variable":
                        {
                            "from_place": new_,
                            "type": [
                                {
                                    "text": "请先选择上面一项",
                                    "value": "None-2"
                                }
                            ],
                            "state": "请选择",
                            "select_1": "请选择",
                            "select_2": "先选择上面的选项"
                        }
                }
            }
            return ka_pian2
        elif msg['value']['done'] =='edit':
            ka_pian13 = {
                "config": {
                    "enable_forward": True,
                    "update_multi": True
                },
                "elements": [
                    {
                        "tag": "markdown",
                        "content": "**你已订阅的栏目有：**\n${lists}",
                        "text_align": "left"
                    },
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": "选择器：请选择要删除哪一个？"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "select_static",
                                "placeholder": {
                                    "tag": "plain_text",
                                    "content": "${from_1}"
                                },
                                "options": []
                            }
                        ]
                    },
                    {
                        "tag": "div",
                        "text": {
                            "content": "删除一次后可以再次选择，继续删除；\n当你完成之后点击下方的按钮。",
                            "tag": "plain_text"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "我已完成"
                                },
                                "type": "primary",
                                "value": {
                                    "done": "done"
                                }
                            }
                        ]
                    }
                ],
                "header": {
                    "template": "blue",
                    "title": {
                        "content": "南开简报-订阅编辑",
                        "tag": "plain_text"
                    }
                }
            }
            find_handle = user_sub.query.filter_by(user_open_id=open_id, place='fs').all()
            if find_handle == []:
                ka_pian13['elements'] = [
                    {'tag': 'markdown', 'content': '**噢，你貌似没有订阅？**', 'text_align': 'left'}]
                text_content2 = json.dumps(ka_pian13)
                type = 'interactive'
                message_api_client.send('open_id', open_id, type, text_content2)
                return 1
            else:
                m = str()
                num = 1
                for i in find_handle:
                    m += f'{num}.{i.sub_place}-{i.sub_type}\n'
                    num += 1
                    ka_pian13['elements'][2]['actions'][0]['options'].append({'text': {
                        "tag": "plain_text",
                        "content": f"{i.sub_place}-{i.sub_type}"}, 'value': 'del:' + f"{i.sub_place}-{i.sub_type}"}
                    )
                ka_pian13['elements'][0]['content'] = ka_pian13['elements'][0]['content'].replace('${lists}', m)
                ka_pian13['elements'][2]['actions'][0]['placeholder']['content'] = \
                    ka_pian13['elements'][2]['actions'][0]['placeholder']['content'].replace('${from_1}', '请选择')
            return ka_pian13


    return None


@app.route("/", methods=["POST"])
def callback_event_handler():
    # init callback instance and handle
    # with open('da.txt', 'ab') as a:
    #     a.write(request.data + '\n\n'.encode())

    if 'action' in request.get_json():
        msg = request.get_json()
        open_user_id = msg['open_id']
        n = ka_pian_handle(msg['action'], open_user_id)
        if n != None:
            return jsonify(n)
        else:
            raise Exception("未知的卡片操作")

    event_handler, event = event_manager.get_handler_with_event(VERIFICATION_TOKEN, ENCRYPT_KEY)

    return event_handler(event)


@app.route("/", methods=['GET'])
@cache.cached(timeout=3600)
def e():
    data = Dean.query.order_by(Dean.push_time.desc()).limit(9)
    # 使用sort()函数在原列表上进行排序
    new_content = []
    for i in data:
        info = {
            'from_place': i.from_place,
            'type': i.type,
            'title': i.title,
            'url': i.url,
            'time_push': i.time_push
        }
        new_content.append(info)

    return render_template('base3.html',first=new_content)


@app.route("/get_data")
def e2():
    with app.app_context():
        if request.args.get('count') == None:
            print('count is None')
            return abort(404)
        if request.args.get('delta') == None:
            return abort(404)
        count = int(request.args.get('count'))
        delta = int(request.args.get('delta'))
        # 获取最近的10条数据，从第10条开始，到第20条结束
        data = Dean.query.order_by(Dean.push_time.desc()).offset(count-1).limit(delta)
        try:
            new_content = []
            for i in data:
                info = {'from_place': i.from_place,
                        'type': i.type,
                        'title': i.title,
                        'url': i.url,
                        'time_push': i.time_push}
                new_content.append(info)
        except IndexError:
            new_content = ""
        response = make_response(jsonify({"data": new_content}))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"

    return response

@app.route('/js')
def e4():
    js_path = f'templates/jquery-3.6.0.min.js'
    try:
        return send_file(js_path, mimetype='text/javascript')
    except Exception as e:
        logger.exception('发生错误！')
@app.route('/pic/<pic_file>')
def e3(pic_file):
    image_path = f'img/{pic_file}'  # 替换为实际的图片路径
    try:
        return send_file(image_path, mimetype='image/jpeg')
    except Exception as e:
        logger.exception('发生错误！')
        return send_file('img/default.jpg', mimetype='image/jpeg')


@app.route('/creative_server', methods=['GET'])
def e36():
    from page_creative_server import encrypt_text
    html = requests.get('http://127.0.0.1:1222/creative_server', params={'id': encrypt_text}).text
    return html



@app.route("/api/check",methods=['GET'])
def e37():
    with app.app_context():
        ask = request.args.get('i')
        header = request.args.get('header')
        if ask == None:
            return jsonify({'data':'None'})
        if header != 'NK_JB':
            return jsonify(abort(404))
        data = Dean.query.filter(Dean.title.like(f'%{ask}%')).all()
        # 使用sort()函数在原列表上进行排序
        data.sort(key=lambda x: x.push_time, reverse=True)
        try:
            new_content = []
            for i in data:
                info = {'from_place': i.from_place,
                        'type': i.type,
                        'title': i.title,
                        'url': i.url,
                        'time_push': i.time_push}
                new_content.append(info)

        except IndexError:
            new_content = ""
    return render_template('check1.html',data=new_content)

if __name__ == "__main__":
    # init()
    # app.run(host="0.0.0.0", port=3001, debug=False)
    serve(app,host='0.0.0.0',port=3001)
# 模块里需要登录的网站有 南开大学官网、商学院网站