import scrapy

from toolkit.crawler.scrapy.failure import FailureHandler
from toolkit.logger import logger


class BaseSpider(scrapy.Spider):
    """
    Base spider class with common methods for handling HTTP responses and failures.
    """

    @staticmethod
    def is_bad_status(response):
        """
        Checks if the response status code indicates a bad response (>= 400).

        :param response: the HTTP response object
        :returns: True if the response is a bad status, False otherwise
        """
        return not response.status or response.status >= 400

    @staticmethod
    def get_status(response):
        """
        Retrieves the HTTP status code from the response.

        :param response: the HTTP response object
        :returns: the status code of the response
        """
        return response.status

    def handle_failure(self, failure):
        """
        Delegates failure handling to the FailureHandler class.

        :param failure: the failure object containing error details
        :returns: response object handled by the FailureHandler
        """
        return FailureHandler.handle_failure(failure, self)
