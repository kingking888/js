# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/3/23
# @File     : track_17.py
# @Software : PyCharm
import json
import execjs
import requests


def get_js(filename):
    f = open(filename, 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


js_str = get_js('track_17.js')
ctx = execjs.compile(js_str)
# data = {"data": [{"num": "00340434328069957517", "fc": 0, "sc": 0}], "guid": "", "timeZoneOffset": -480}
data = {"data": [{"num": "00340434328069957517", "fc": 0, "sc": 0}, {"num": "00340434328070021641", "fc": 0, "sc": 0}],
        "guid": "", "timeZoneOffset": -480}
last_event_id = ctx.call("get_last_event_id", json.dumps(data))
print(last_event_id)
cookies = {
    "v5_TranslateLang": "zh-Hans",
    "Last-Event-ID": last_event_id
}
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-length": "87",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://t.17track.net",
    "referer": "https://t.17track.net/zh-cn",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"}
url = 'https://t.17track.net/restapi/track'
# 添加ip资源
res = requests.post(url, headers=headers,  cookies=cookies, data=json.dumps(data)
                    , proxies={'https': 'http://104.227.9.95:8800', 'http': 'http://104.227.9.95:8800'}
                    )
print(res.text)
