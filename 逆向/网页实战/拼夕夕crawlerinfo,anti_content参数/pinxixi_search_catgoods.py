# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/5/6
# @File     : pinduoduo.py
# @Software : PyCharm
"""
商品列表页信息抓取，需账号
"""
import requests
import json
import re
import execjs
import copy
import time
import logging
import pymongo
import pytz
import datetime
import random
from pymongo.operations import UpdateOne
from logging import handlers


def get_local_time():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now().replace(tzinfo=tz)


def get_js(filename):
    f = open(filename, 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


def get_anti_info(cookie: str, url: str, useragent: str):
    js_content = get_js('anti_content.js')
    ctx = execjs.compile(js_content)
    info = ctx.call("get_anti_content", cookie, url, useragent)
    return info


def get_cookie_to_str(cookie: dict):
    new_cookie_list = []
    for k, v in cookie.items():
        cookie_split = "{}={}".format(k, v)
        new_cookie_list.append(cookie_split)
    cookie_str = '; '.join(new_cookie_list)
    if ' _nano_fp' not in cookie_str:
        cookie_str += '; '
    return cookie_str


class MongoClient(object):
    HOST = '127.0.0.1'
    PORT = 27017

    @classmethod
    def GetConnection(cls, db):
        client = pymongo.MongoClient(host=cls.HOST, port=cls.PORT)
        # mydb = client.admin
        # mydb.authenticate(cls.USERNAME, cls.PASSWORD, mechanism='SCRAM-SHA-1')
        return client[db]


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


class Pinduoduo:
    def __init__(self, hub_url, base_url, token, useragent):
        self.hub_url = hub_url
        self.base_url = base_url
        self.token = token
        self.useragent = useragent
        self.current_page = 1
        self.log = Logger('pinduoduo_list.log', level='debug')
        self.mongo_db = MongoClient.GetConnection('pinduoduo')
        self.get_session()

    def get_session(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "AccessToken": self.token,
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "mobile.yangkeduo.com",
            "Pragma": "no-cache",
            "Referer": self.hub_url,
            "User-Agent": self.useragent
        }
        my_cookies = {
            "PDDAccessToken": self.token,
            "webp": "1"
        }
        self.session = requests.session()
        # 添加必要cookie参数及header参数
        self.session.headers = headers
        requests.utils.add_dict_to_cookiejar(self.session.cookies, my_cookies)

    def get_hub_page_info(self):
        # 访问hub页面
        try:
            hub_res = self.session.get(hub_url)
            first_res = hub_res.text
            first_origin_data = re.findall('window\.rawData=(.*?);\s', first_res)[0]
            first_json_data = json.loads(first_origin_data)

            product_list_info = first_json_data['store']['data']['ssrListData']['list']
            self.save_data(product_list_info)
        except Exception as e:
            print(e)
            self.log.logger.error('当前进行第%s页信息抓取，出现验证码' % self.current_page)
            self.log.logger.warning(str('cookie:%s\n' % str(self.session.cookies)))
            return None
        # 更新cookie的pdd_vds
        self.session.get('http://mobile.yangkeduo.com/csr/comm_prefetch_goods.html')
        return first_json_data

    def get_second_page_info(self):
        # 第二次访问
        first_json_data = self.get_hub_page_info()
        if not first_json_data:
            return None, None
        self.current_page += 1
        # 添加访问参数
        second_request_params = first_json_data['store']['data']['ssrListData']['nextRequestParams']
        second_request_params["opt_source"] = "search_opt_goods"
        second_request_params['pdduid'] = self.session.cookies.get('pdd_user_id')
        cookie_str_2 = get_cookie_to_str(self.session.cookies)
        info = get_anti_info(cookie_str_2, self.base_url, self.useragent)
        second_request_params['anti_content'] = info[0]
        # 添加相应cookie参数
        _nano_fp_list = info[1].split(';')[-1].split('=')
        my_cookies_v2 = {_nano_fp_list[0]: _nano_fp_list[1]}
        requests.utils.add_dict_to_cookiejar(self.session.cookies, my_cookies_v2)
        try:
            second_res = self.session.get(base_url, params=second_request_params)
            second_request_response = second_res.json()
            self.save_data(second_request_response['goods_list'])
        except Exception as e:
            print(e)
            self.log.logger.error('当前进行第%s页信息抓取，出现验证码' % self.current_page)
            self.log.logger.warning(str('参数:%s\n' % second_request_params + 'cookie:%s\n' % str(self.session.cookies)))
            return None, None
        return second_request_params, second_request_response

    def get_other_page(self, old_request_params, request_response):
        # 递归终止条件goods_list = []，或者爬取数据过程异常
        time.sleep(random.uniform(0, 2))
        self.current_page += 1
        if not request_response.get('goods_list'):
            self.log.logger.info('当前进行第%s页信息抓取，已经无下一页参数' % self.current_page)
            return
        request_params = copy.deepcopy(old_request_params)
        request_params['flip'] = request_response['flip']
        request_params['offset'] = request_response['flip'].split(';')[0]
        cookie_str = get_cookie_to_str(self.session.cookies)
        request_params['anti_content'] = get_anti_info(cookie_str, self.base_url, self.useragent)[0]
        res = self.session.get(base_url, params=request_params)
        cookie = json.dumps(dict(self.session.cookies))
        try:
            new_request_response = copy.deepcopy(res.json())
            if not new_request_response.get('goods_list'):
                self.log.logger.info('当前进行第%s页信息抓取，已经无下一页参数' % self.current_page)
                return
            self.save_data(new_request_response['goods_list'])
            self.log.logger.info('当前完成第%s页信息抓取' % self.current_page)
        except Exception as e:
            print(e)
            new_request_response = {}
            self.log.logger.error('当前进行第%s页信息抓取，出现验证码' % self.current_page)
            self.log.logger.warning(str('参数:%s\n' % request_params + 'cookie:%s\n' % cookie))
        # 递归抓取下页数据
        self.get_other_page(request_params, new_request_response)

    def save_data(self, data_list):
        collection = self.mongo_db['product_list']
        update_list = []
        for data in data_list:
            if data.get('goodsID'):
                data['goods_id'] = data.get('goodsID')
                data['is_hub'] = True
                data.pop('goodsID')
            data['update_time'] = get_local_time()
            update_list.append(UpdateOne({'goods_id': data.get('goods_id')}, {"$set": data}, upsert=True))
        collection.bulk_write(update_list, ordered=True)
        self.log.logger.info("完成数据存储,数据总数%s" % len(data_list))

    def main(self):
        second_page_info = self.get_second_page_info()
        if None in second_page_info:
            return
        second_request_params, second_request_response = second_page_info
        self.get_other_page(second_request_params, second_request_response)


if __name__ == '__main__':
    # 耳机主页，耳机品类id:opt_id=10482
    # hub_url = 'http://mobile.yangkeduo.com/search_catgoods.html?opt_id=10482'
    # # api接口地址
    # base_url = 'http://mobile.yangkeduo.com/proxy/api/api/search/opt/10482/groups?'
    # AccessToken = "DGPGBT3MWVBSEPZWZXG7SHVQKR43R6Q2CXJBJKBWLQ4DZJCUEISA111818a"
    # useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    # pinduoduo = Pinduoduo(hub_url, base_url, AccessToken, useragent)
    # pinduoduo.main()

    pass
