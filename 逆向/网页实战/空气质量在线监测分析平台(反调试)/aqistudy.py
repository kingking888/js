# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/4/10
# @File     : aqistudy.py
# @Software : PyCharm
import requests
import json

url = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'

data = {
    'h0lgYxgR3': "eyJhcHBJZCI6ImJhZWM5OGE3M2MxYmZmNzk2NjAzY2IyZmE5ZDZkNDQ5IiwibWV0aG9kIjoiR0VUREFUQSIsInRpbWVzdGFtcCI6MTYxODA0MzIzNTk2MiwiY2xpZW50dHlwZSI6IldFQiIsIm9iamVjdCI6eyJjaXR5Ijoi5p2t5beeIn0sInNlY3JldCI6ImIxMjAxMTMxYTJmMGYwZjMwNWI0OTFkMDJkOTMxMGRiIn0="
}

res = requests.post(url, data)
print(res.text)
