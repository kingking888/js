# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/4/8
# @File     : douyin.py
# @Software : PyCharm
import requests
import execjs
import urllib.parse as urlparse
import re
import brotli


url = 'https://v.douyin.com/WqMX9d/'
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}
session = requests.session()
session.headers = headers

res = session.get(url)
redirect_url = res.url
parsed = urlparse.urlparse(redirect_url)
querys = urlparse.parse_qs(parsed.query)
querys = {k: v[0] for k, v in querys.items()}
sec_uid = querys.get("sec_uid")
u_id = re.findall('user/(\d+)', redirect_url)[0]
print(u_id,)

def get_js(filename):
    f = open(filename, 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


js_str = get_js('douyin.js')
ctx = execjs.compile(js_str)
_signature = ctx.call("generateSignature", u_id)

data = {
    "sec_uid": sec_uid,
    "count": "21",
    "max_cursor": "0",
    "aid": "1128",
    "_signature": _signature,
    "dytk": ""
}
base_url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?'
res_list = session.get(base_url, params=data)
print(res_list.url)
# 有问题,方案二将headers中的accept-encoding的br删除
# if res_list.headers.get('Content-Encoding') == 'br':
#     data = brotli.decompress(res_list.content).decode("utf-8")

print(res_list.text)

