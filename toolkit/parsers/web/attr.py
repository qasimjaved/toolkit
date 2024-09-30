from typing import List, Optional, Union
from scrapy.http import Response
from urllib.parse import urljoin, urlparse


def parse_attr(response: Optional[Response], xpaths: Optional[List[str]] = None,
               attr: str = 'href', _abs: bool = True,
               extract_all: bool = False, unique: bool = True,
               same_domain: bool = False, join_with: Optional[str] = None) -> Optional[Union[str, List[str]]]:
    """
    Parse attributes from the response/selector object for specified xpath(s).

    :param response: Scrapy response object.
    :param xpaths: List of xpath expressions (if None, extract all attribute values).
    :param attr: Attribute name to extract.
    :param _abs: Flag to return absolute URL.
    :param extract_all: Flag to indicate if all attribute values should be returned as a single string.
    :param unique: Flag to indicate if only unique attribute values should be returned.
    :param same_domain: Flag to indicate if only attributes from the same domain should be returned.
    :param join_with: String to join results if extract_all is True. Defaults to None.

    :return: Parsed attribute value(s) from the xpath(s).
    """
    if xpaths is None:
        # If no xpaths are provided, extract all attribute values from the response
        attr_values = response.xpath(f"//@{attr}").extract()
    else:
        attr_values = _extract_attributes(response, xpaths, attr)

    if _abs:
        attr_values = _convert_to_absolute_urls(response, attr_values)

    if same_domain:
        base_url = response.request.url
        attr_values = [url for url in attr_values if _is_same_domain(base_url, url)]

    if unique:
        attr_values = list(set(attr_values))  # Get unique values

    return _return_attributes(attr_values, extract_all, join_with)


def _extract_attributes(response: Optional[Response], xpaths: List[str], attr: str) -> List[str]:
    """
    Extract attribute values from the response for the given xpaths.

    :param response: Scrapy response object.
    :param xpaths: List of xpath expressions.
    :param attr: Attribute name to extract.

    :return: List of extracted attribute values.
    """
    for xpath in xpaths:
        values = response.xpath(f"{xpath}/@{attr}").extract()
        if values:
            return values
    return []


def _convert_to_absolute_urls(response: Response, urls: List[str]) -> List[str]:
    """
    Convert relative URLs to absolute URLs based on the response object.

    :param response: Scrapy response object.
    :param urls: List of URLs to convert.

    :return: List of absolute URLs.
    """
    return [_convert_to_absolute_url(response, url) for url in urls]


def _convert_to_absolute_url(response: Response, url: str) -> str:
    """
    Gets an absolute URL from a relative URL based on the response's base URL.

    :param response: Scrapy response object.
    :param url: Relative URL to convert to absolute.

    :return: Absolute URL.
    """
    base_url = response.meta.get("url") or response.request.url
    return urljoin(base_url, url)


def _is_same_domain(base_url: str, url: str) -> bool:
    """
    Check if the given URL is in the same domain as the base URL.

    :param base_url: The base URL to compare against.
    :param url: The URL to check.

    :return: True if the URL is in the same domain, False otherwise.
    """
    base_domain = urlparse(base_url).netloc
    url_domain = urlparse(url).netloc
    return base_domain == url_domain


def _return_attributes(attr_values: List[str], extract_all: bool, join_with: Optional[str]) -> Optional[Union[str, List[str]]]:
    """
    Return a single attribute value, a list of attribute values, or a joined string of attribute values
    based on the extract_all flag.

    :param attr_values: List of extracted attribute values.
    :param extract_all: Flag to indicate if all attribute values should be returned as a single string.
    :param join_with: String to join attribute values if extract_all is True. Defaults to None.

    :return: A list of attribute values or a single joined string.
    """
    if extract_all:
        return join_with.join(attr_values) if join_with else attr_values
    return attr_values if attr_values else None
