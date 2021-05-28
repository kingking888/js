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
from aiohttp_socks import ProxyConnector


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
        connector = ProxyConnector.from_url('socks5://user:password@127.0.0.1:1080')
        ### or use ProxyConnector constructor
        # connector = ProxyConnector(
        #     proxy_type=ProxyType.SOCKS5,
        #     host='127.0.0.1',
        #     port=1080,
        #     username='user',
        #     password='password',
        #     rdns=True
        # )

        ### proxy chaining (since ver 0.3.3)
        # connector = ChainProxyConnector.from_urls([
        #     'socks5://user:password@127.0.0.1:1080',
        #     'socks4://127.0.0.1:1081',
        #     'http://user:password@127.0.0.1:3128',
        # ])
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(request.url) as response:
                # await response.text()
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
