# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/5/28
# @File     : start.py
# @Software : PyCharm
import asyncio
from twisted.internet import asyncioreactor
from scrapy import cmdline

asyncioreactor.install(asyncio.get_event_loop())

if __name__ == '__main__':
    cmdline.execute("scrapy crawl httpbin".split())
