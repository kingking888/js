# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class MyTestSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyTestDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


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
        connector = ProxyConnector.from_url('socks5://xxx.xxx.xxx.xxx:xxx')
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
                content = await response.read()
                response = HtmlResponse(
                    request.url,
                    status=response.status,
                    headers=response.headers,
                    body=content,
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
