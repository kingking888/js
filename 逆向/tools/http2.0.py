# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/5/21 下午6:10
# @Author : artio
# @File : p10.py
# @version    : v1.0
# @editor : artio
# @desc: 功能模块 功能概述

import urllib3.util.ssl_

# 处理协议
urllib3.util.ssl_.DEFAULT_CIPHERS = ":".join(
    i for i in urllib3.util.ssl_.DEFAULT_CIPHERS.split(":") if not i.startswith("!"))

from requests import Session
from hyper.contrib import HTTP20Adapter
from requests.utils import CaseInsensitiveDict

_request = Session.request


class MyHTTP20Adapter(HTTP20Adapter):
    def __init__(self, *args, **kwargs):
        super(MyHTTP20Adapter, self).__init__(*args, **kwargs)
        super(HTTP20Adapter, self).__init__(*args, **kwargs)


def request(self, method, url, clear_headers=False, http2=False, **kwargs):
    # 处理h2
    if http2:
        self.mount("https://", MyHTTP20Adapter())
    # 处理 headers顺序
    if clear_headers:
        self.headers = CaseInsensitiveDict()
    result = _request(self, method=method, url=url, **kwargs)
    return result


Session.request = request

headers = {
    ':method': 'POST',
    ':authority': 'www.python-spider.com',
    ':scheme': 'https',
    ':path': '/api/challenge10',
    'content-length': '6',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.python-spider.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.python-spider.com/challenge/10',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1621530105; no-alert=true; sessionid=6uhjsr25pmjej57vsg2r6gi4r7yqzc3w; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1621592292',

}

if __name__ == '__main__':
    import requests

    url = 'https://www.python-spider.com/api/challenge10'
    c = 0
    for page in range(1, 101):

        res = requests.post(url, http2=True, data={"page": page}, verify=False, headers=headers, clear_headers=True)
        print(res.text)
        for data in res.json()['data']:
            c += int(data['value'].strip())
    print(c)
