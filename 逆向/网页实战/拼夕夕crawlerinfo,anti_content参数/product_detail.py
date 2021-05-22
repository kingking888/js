# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/5/10
# @File     : product_detail.py
# @Software : PyCharm
import requests
from pinxixi_search_catgoods import MongoClient, Logger, get_local_time
import json
import re
import random
import time
import traceback
import tqdm
from urllib.parse import quote


class PinduoduoProduct:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "mobile.yangkeduo.com",
        "Pragma": "no-cache",
        "Referer": "http://mobile.yangkeduo.com/search_catgoods.html?opt_id=10482",
        "Upgrade-Insecure-Requests": "1",
    }

    hub_url = 'http://mobile.yangkeduo.com/'

    def __init__(self):
        mondo_db = MongoClient.GetConnection('pinduoduo')
        self.product_list_table = mondo_db['product_list']
        self.product_info_table = mondo_db['product']
        self.session = requests.session()
        self.session.headers = self.headers
        self.log = Logger('pinduoduo_product.log', level='debug')
        self.total_size = 0
        self.remain_task_num = 0

    def get_product_urls(self):
        product_ids = self.product_info_table.distinct('goodsID')
        product_count = self.product_list_table.count_documents(
            {"goods_id": {"$nin": product_ids}}
        )
        self.total_size = product_count
        self.remain_task_num = product_count
        product_urls_query = self.product_list_table.find(
            {"goods_id": {"$nin": product_ids}},
            {"linkURL": 1, "link_url": 1, "goods_id": 1, "_id": 0})
        for info in product_urls_query:
            product_url = info.get('linkURL') if info.get('linkURL') else info.get('link_url')
            yield product_url

    def run(self, herders_config: dict):
        requests.utils.add_dict_to_cookiejar(self.session.cookies, herders_config.get('cookie'))
        self.session.headers["User-Agent"] = herders_config.get('useragent')
        for url in self.get_product_urls():
            product_info = self.get_info(url)
            if product_info:
                self.remain_task_num -= 1
                self.log.logger.info(
                    '当前进行商品详情{}抓取，总任务数:{}，剩余任务数:{}'.format(
                        product_info.get('goodsID'), self.total_size, self.remain_task_num))
            else:
                break

    def get_info(self, url):
        time.sleep(random.uniform(0, 5))
        product_url = self.hub_url + url
        res = self.session.get(product_url)
        try:
            origin_data = re.findall('window\.rawData=(.*?);\s+</script>', res.text)[0]
            json_data = json.loads(origin_data)
            product_info = json_data['store']['initDataObj']['goods']
            self.save_data(product_info)
            return product_info
        except:
            traceback.print_exc()
            self.log.logger.error('当前进行地址%s信息抓取，出现验证码' % product_url)
            self.log.logger.warning('验证码地址%s' % res.url)
            self.log.logger.warning(str('headers参数:%s\n' % self.headers + 'cookie:%s\n' % self.session.cookies))
            return None

    def save_data(self, data):
        if not data.get('goodsID'):
            print('错误信息，未存储')
            return
        data['update_time'] = get_local_time()
        self.product_info_table.update_one({"goodsID": data.get('goodsID')}, {'$set': data}, upsert=True)
        self.log.logger.info("完成数据存储,商品id:%s" % data.get('goodsID'))


if __name__ == '__main__':
    # 该cookie绑定账号及相应的useragent
    UserAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    Cookie = {
        "PDDAccessToken": "6K3PJOCST2BOHNLI5Y5ONGGHMWBKKEFCE6LTBQ5YCYHTCPZ6SL7Q110e3bb",
        "pdd_user_id": "3449836316899",
        "pdd_user_uin": "M72R6IPXS7H53HXNW24AHY3FIM_GEXDA",
        "api_uid": "CkuQ12Coq6CIZwBUZQm/Ag==",
        "_nano_fp": "XpExX0EYXpmbnpdbnC_bTl7jw3PCFfNvxabzWjbt",
        "ua": quote(UserAgent, safe='()'),
        "webp": "1",
        "pdd_vds": "gaLfNdyDGTPfnNNmysbBOnGwNNbBauGlbeIeGfbsEuQBQwouGwEmnbnfOwol"
    }
    product = PinduoduoProduct()
    dic = {'cookie': Cookie, 'useragent': UserAgent}
    product.run(dic)
