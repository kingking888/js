# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/3/22
# @File     : pratice_6.py
# @Software : PyCharm

import requests


class TestSession:
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "6",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "sessionid=wjw55bd67ewb4v281dsegc3k7df39evs; Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1616142473; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1616380635",
        "Host": " www.python-spider.com",
        "Origin": "http://www.python-spider.com",
        "Referer": "http://www.python-spider.com/challenge/6",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    def __init__(self, session=None):
        self.session = session
        if not session:
            self.session = requests.session()

    def post(self, *args, **kwarg):
        try:
            response = self.session.post(*args, **kwarg)
            return response
        except Exception as e:
            print(e)


if __name__ == '__main__':
    session = TestSession()
    url = 'http://www.python-spider.com/api/challenge6'
    data_list = []
    for i in range(1, 101):
        data = {'page': i}
        res = session.post(url, data=data)
        res_json = res.json()
        print(res_json)
        data_list.extend(res_json.get('data'))
    values = [int(info["value"].strip()) for info in data_list]
    total = sum(values)
    print(total)
