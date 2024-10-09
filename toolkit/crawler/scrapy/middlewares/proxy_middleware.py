# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from os import getenv

from scrapy import signals

from toolkit.logger import logger


PROXY_USER = 'scraperapi'
PROXY_KEY = getenv('SCRAPER_API_KEY')
PROXY_HOST = 'proxy-server.scraperapi.com:8001'


class ProxyMiddleware:
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
        # Select a random proxy
        try:
            if request.meta.get('url'):
                return
            proxy_url = f'http://{PROXY_USER}:{PROXY_KEY}@{PROXY_HOST}'
            request.meta['url'] = request.url
            # logger.info(f"Adding proxy: {proxy_url}")
            # request.meta['proxy'] = proxy_url
        except Exception as e:
            logger.exception(e)

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
        spider.logger.info("Spider opened: %s" % spider.name)
