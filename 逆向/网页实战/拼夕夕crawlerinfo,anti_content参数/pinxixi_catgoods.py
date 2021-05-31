# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/5/20
# @File     : pinxixi_catgoods.py
# @Software : PyCharm
"""
商品列表页信息抓取，需账号
"""
import requests
import json
import re
import copy
import time
import random
from pymongo.operations import UpdateOne
from crawers.pdd.pinxixi_search_catgoods import get_local_time, get_js, get_anti_info, get_cookie_to_str, MongoClient, \
    Logger


class Pinduoduo:
    def __init__(self, hub_url, base_url, token, useragent):
        self.hub_url = hub_url
        self.opt_id = re.findall('opt_id=(\d+)', self.hub_url)[0]
        self.base_url = base_url
        self.token = token
        self.useragent = useragent
        self.current_page = 1
        self.log = Logger('pinduoduo_catgoods_list.log', level='debug')
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

            product_list_info = first_json_data['store']['tabListMap'][self.opt_id]['tabGoodsList']['list']
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
        # todo:添加访问参数,offset,opt_type相关参数请从网页核对
        second_request_params = {"offset": 40, "count": 20, 'page_sn': '10028', 'support_types': '0_4', 'opt_type': 2}
        second_request_params["list_id"] = first_json_data['store']['tabListMap'][self.opt_id]['tabGoodsList']['listId']
        second_request_params['opt_id'] = first_json_data['store']['currentOptId']
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
        request_params['offset'] = self.current_page * 20  # 20为一页
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
    # 需更改opt_id
    # # 灯饰照明
    # hub_url = 'http://mobile.yangkeduo.com/catgoods.html?opt_id=1942&opt_type=2'
    # base_url = 'http://mobile.yangkeduo.com/proxy/api/api/caterham/query/subfenlei_gyl_label?'
    # AccessToken = "6K3PJOCST2BOHNLI5Y5ONGGHMWBKKEFCE6LTBQ5YCYHTCPZ6SL7Q110e3bb"
    # useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    # pinduoduo = Pinduoduo(hub_url, base_url, AccessToken, useragent)
    # pinduoduo.main()

    # hub_url = 'http://mobile.yangkeduo.com/catgoods.html?opt_id=307&opt_type=2'
    # base_url = 'http://mobile.yangkeduo.com/proxy/api/api/caterham/query/subfenlei_gyl_label?'
    # AccessToken = "6K3PJOCST2BOHNLI5Y5ONGGHMWBKKEFCE6LTBQ5YCYHTCPZ6SL7Q110e3bb"
    # useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    # pinduoduo = Pinduoduo(hub_url, base_url, AccessToken, useragent)
    # pinduoduo.main()

    # 泳装用品
    hub_url = 'http://yangkeduo.com/catgoods.html?refer_page_name=index&opt_id=1458&opt_type=2'
    base_url = 'http://mobile.yangkeduo.com/proxy/api/api/caterham/query/subfenlei_gyl_label?'
    AccessToken = "PZPYE676LIMWFLTIQHFM6SYVGVR5CZ7LHEFJJTI6PFTBQT3TDG4A110e3bb"
    useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    pinduoduo = Pinduoduo(hub_url, base_url, AccessToken, useragent)
    pinduoduo.main()
