# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/3/29
# @File     : shtdsc.py
# @Software : PyCharm
import requests
import re

url = 'http://www.shtdsc.com/2016/tdjy/dkjs/'
js_url = 'http://www.shtdsc.com/4QbVtADbnLVIc/c.FxJzG50F.dfe1675.js'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "www.shtdsc.com",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
session = requests.session()
session.headers = headers

res = session.get(url,proxies={'http': 'http:127.0.0.1:8888'})
index_text = res.text
# print(index_text)
# print(session.cookies)
# _$ts文件
_ts_res = session.get(js_url,proxies={'http': 'http:127.0.0.1:8888'})

print(_ts_res.text)
print('aaa')

# 内嵌js文件
js_content = re.findall('r="m">([\s\S]*?)\s*</script>', index_text)
print(js_content[0])
print('aaa')

# html文本，包括content
html = re.sub("""r=["']m["']>([\s\S]*?)\s*</script>""", 'r="m"></script>', index_text)
print(html)
print('aaa')



