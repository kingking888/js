# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/4/10
# @File     : cnpcbidding.py
# @Software : PyCharm
import requests

url = 'https://www.cnpcbidding.com/cms/pmsbidInfo/homePage'

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.cnpcbidding.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.cnpcbidding.com/html/1/index.html',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'X-Requested-With': "XMLHttpRequest"
}

res = requests.get(url, headers=headers)
print(res.text)

# 再进入事件监听看到eval,可以看到是有加密解密过程,对应的跟下去就好
