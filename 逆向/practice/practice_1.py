# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/3/19
# @File     : practice_1.py
# @Software : PyCharm

import requests
import time
import base64
import execjs


def get_js():
    f = open("./1.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


def get_request_info(data):
    base_url = 'http://www.python-spider.com/challenge/api/json'
    timestamp = str(time.time())[0:10]
    a = '9622'
    base64_safe = base64.b64encode((a + timestamp).encode("latin1")).decode("utf8")
    js_str = get_js()
    ctx = execjs.compile(js_str)
    safe = ctx.call("hex_md5", base64_safe)
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1616130804; no-alert=true; sessionid=743dkv62vsuzg0xpzqc9a5btxb08zdom; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1616132007",
        "Host": "www.python-spider.com",
        "Referer": "http://www.python-spider.com/challenge/1",
        "safe": safe,
        "timestamp": timestamp,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    try:
        res = requests.get(base_url, headers=headers, params=data)
        info = res.json().get('infos')
        return info
    except Exception as e:
        print(e)


if __name__ == '__main__':
    infos_list = []
    for i in range(1, 41):
        data = {"page": i, "count": 30}
        infos = get_request_info(data)
        infos_list.extend(infos)
    count = 0
    for info in infos_list:
        if '招' in info.get("message"):
            count += 1
            print(info.get("message"))
    print(count)

