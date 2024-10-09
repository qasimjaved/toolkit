
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TCPTimedOutError, TimeoutError

from toolkit.logger import logger


class FailureHandler:
    """
    Handles various types of request failures and creates appropriate responses.

    :param failure: the failure object containing error details
    :returns: a response object after handling the failure
    """

    @staticmethod
    def handle_failure(failure, spider):
        """
        Main failure handler that delegates handling to specific methods based on failure type.

        :param failure: the failure object containing error details
        :param spider: the spider instance calling this handler
        :returns: a response object or calls spider's parse method with the appropriate response
        """
        logger.info("Handling failure for request: %s", failure.request.url)

        if failure.check(HttpError):
            return FailureHandler._handle_http_error(failure, spider)
        elif failure.check(TimeoutError, TCPTimedOutError):
            return FailureHandler._handle_timeout(failure.request, spider)
        else:
            return FailureHandler._handle_generic_failure(failure, spider)

    @staticmethod
    def _handle_http_error(failure, spider):
        """
        Handles HTTP errors by logging the error and retrying the response.

        :param failure: the failure object containing the HTTP error
        :param spider: the spider instance calling this handler
        :returns: the result of retrying the request
        """
        response = failure.value.response
        logger.error("HTTP Error on %s, status: %d", response.url, response.status)
        return spider.parse(response)

    @staticmethod
    def _handle_timeout(request, spider):
        """
        Handles timeout errors by creating a fake response and logging the timeout.

        :param request: the original request object that timed out
        :param spider: the spider instance calling this handler
        :returns: a fake response with a 504 status
        """
        logger.error("Timeout Error on %s", request.url)
        fake_response = scrapy.http.HtmlResponse(
            url=request.url, status=504, body=b"Timeout", request=request
        )
        return spider.parse(fake_response)

    @staticmethod
    def _handle_generic_failure(failure, spider):
        """
        Handles generic request failures and logs an unknown error.

        :param failure: the failure object for the generic error
        :param spider: the spider instance calling this handler
        :returns: a fake response with a 600 status indicating an unknown error
        """
        request = failure.request
        logger.error("Unknown failure on %s", request.url)
        fake_response = scrapy.http.HtmlResponse(
            url=request.url, status=600, body=b"Unknown error", request=request
        )
        return spider.parse(fake_response)
