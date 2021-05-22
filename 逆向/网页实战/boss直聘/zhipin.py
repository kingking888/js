# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/3/30
# @File     : zhipin.py
# @Software : PyCharm
import requests
import execjs


base_url = 'https://www.zhipin.com/job_detail/?'
params = {
    "query": "%E7%88%AC%E8%99%AB",
    "city": "100010000",
    "industry": ""
}
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
session = requests.session()

cookies = {
       '__zp_stoken__': ''
}
requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
session.headers = headers
res = session.get(base_url, params=params)
print(res.url)
print(res.text)
