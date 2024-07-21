#!/usr/bin/env python3.8
class Obj(dict):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Obj(b) if isinstance(b, dict) else b)


def dict_2_obj(d: dict):
    return Obj(d)

def check_ip(ip:str)->dict:
    import requests
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'mode': 'cors',
        'Content-Type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 HBPC/12.1.3.303',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://qifu.baidu.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://qifu.baidu.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    params = {
        'ip': ip,
    }

    response = requests.get('https://qifu-api.baidubce.com/ip/geo/v1/district', params=params, headers=headers)
    a = response.json()
    return a['data']
