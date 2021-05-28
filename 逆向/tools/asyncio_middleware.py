# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/5/28
# @File     : asyncio_middleware.py
# @Software : PyCharm

"""
采用asyncio形式则更换reactor
import asyncio
from twisted.internet import asyncioreactor
asyncioreactor.install(asyncio.get_event_loop())
"""
import asyncio
import aiohttp
from scrapy import signals
from scrapy.http import HtmlResponse
from twisted.internet.defer import Deferred
from scrapy.http import Request
from aiosocksy.connector import ProxyConnector, ProxyClientRequest


def as_deferred(f):
    """Transform a Twisted Deffered to an Asyncio Future"""

    return Deferred.fromFuture(asyncio.ensure_future(f))


class AsyncioMiddleware:

    @classmethod
    async def _from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    @classmethod
    def from_crawler(cls, crawler):
        loop = asyncio.get_event_loop()
        middleware = loop.run_until_complete(
            asyncio.ensure_future(cls._from_crawler(crawler))
        )

        return middleware

    async def _process_request(self, request, spider):
        connector = ProxyConnector()
        socks = 'socks5://127.0.0.1:12377'
        async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session:
            async with session.get(request.url, proxy=socks) as response:
                print(await response.text())
                response = HtmlResponse(
                    request.url,
                    status=response.status,
                    headers=response.headers,
                    body=response.content,
                    encoding=response.get_encoding(),
                    request=request
                )
                return response

    def process_request(self, request, spider):
        if not isinstance(request, Request):
            return None
        return as_deferred(self._process_request(request, spider))

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)
