import scrapy
from scrapy_redis.spiders import RedisSpider


class TestScrapyRedisSpider(RedisSpider):
    name = 'test_scrapy_redis'

    def parse(self, response):
        print(response.text)
        pass

# redis-cli lpush test_scrapy_redis:start_urls http://httpbin.org/ip