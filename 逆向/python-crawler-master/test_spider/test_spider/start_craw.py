# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/3/29
# @File     : start_craw.py
# @Software : PyCharm
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl test_scrapy_redis".split())
