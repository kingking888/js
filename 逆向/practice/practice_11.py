# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/3/22
# @File     : practice_11.py
# @Software : PyCharm

# 加速乐
import requests
import re
import execjs
from lxml import etree


class TestSession:
    cookie = {
        # "Hm_lvt_337e99a01a907a08d00bed4a1a52e35d": "1616142473",
        # "Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d": "1616580378",
        "sessionid": "jfbf7bcmeegq24r6tr8rksdc8w60eu3a",
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "www.python-spider.com",
        "Connection": "keep-alive",
        "Referer": "http://www.python-spider.com/challenge/11",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }

    def __init__(self, session=None):
        self.url = 'http://www.python-spider.com/challenge/11'
        self.session = session
        if not session:
            self.session = requests.session()

    def post(self, *args, **kwarg):
        try:
            response = self.session.post(*args, **kwarg)
            return response
        except Exception as e:
            print(e)

    def get(self, *args, **kwarg):
        try:
            response = self.session.get(*args, **kwarg)
            return response
        except Exception as e:
            print(e)

    def get_jsl_js_code(self):
        res_text = self.get(self.url, headers=self.headers, cookies=self.cookie).text
        base_js_code = res_text.replace('eval', 'return').replace('</script>', '').replace('<script>', '')
        js_code = 'function get_jsl_js(){' + base_js_code + '}'
        with open('4_1.js', 'w+') as f:
            f.write(js_code)
        ctx = execjs.compile(js_code)
        code = ctx.call("get_jsl_js")
        with open('4_2.js', 'w+') as f:
            f.write(code)
        return code

    def get_jsl_cookie(self):
        code = self.get_jsl_js_code()
        # with open('4_2.js', 'r') as f:
        #     code = f.read()
        sub_code_1 = re.sub('setTimeout.*?;', '', code)
        sub_code_2 = re.sub('document\.cookie', 'cookie', sub_code_1)
        sub_code_3 = re.sub('if\(\(function\(\).*', '', sub_code_2)
        sub_code_4 = sub_code_3.replace(
            r"_N=document.createElement('div');_N.innerHTML='<a href=\'/\'>_1H</a>';_N=_N.firstChild.href;var _t=_N.match(/http?:\/\//)[0];_N=_N.substr(_t.length).toLowerCase()",
            '_N="www.python-spider.com/"')
        sub_code_5 = sub_code_4.replace("+';Expires=Tue, 12-Dec-30 09:50:26 GMT;Path=/;'", ';return cookie')
        sub_code_6 = sub_code_5.replace('__jsl_clearance=', '')
        ctx = execjs.compile(sub_code_6)
        cookie = ctx.call("_N")
        return cookie

    def get_res(self):
        jsl_cookie = self.get_jsl_cookie()
        self.cookie['__jsl_clearance'] = jsl_cookie
        print(self.cookie)
        res = session.get(self.url, headers=self.headers, cookies=self.cookie)
        html = etree.HTML(res.text)
        res = html.xpath('//td/text()')
        print(res)
        total = 0
        for info in res:
            total += int(info.strip())
        print(total)


if __name__ == '__main__':
    session = TestSession()
    # res = session.get_jsl_js_code()
    # print(res)
    # cookie = session.get_jsl_cookie()
    # print(cookie)
    session.get_res()
