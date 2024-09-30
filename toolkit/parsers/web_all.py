import html
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from scrapy.http import Request, Response, HtmlResponse
from w3lib.html import remove_tags, remove_tags_with_content
import re

from commons.constants import DISABLED_RETRY_CODES, RETRY_STATUS_CODES
from commons.logger import logger
from commons.enums.enums import CrawlState


def unescape(text: str) -> str:
    """
    Unescape HTML entities
    """
    try:
        return html.unescape(text)
    except:
        return text


def read_file_content(file_path: str) -> str:
    """
    Open up file, reads content & return whole textual content

    :param file_path: file path
    :returns: file content
    """
    file_obj = open(file_path, 'r')
    file_content = file_obj.read()
    file_obj.flush()
    file_obj.close()
    return file_content


def load_html_file(file_path: str, url: str = "None", request: Request = None) -> HtmlResponse:
    """
    Load HTML file content, converts to HtmlResponse object & returns it

    :param file_path: HTML file path
    :param url: URL to set in response object
    :param request: Request object to be set in response object
    :returns: HTML response
    """

    file_content = read_file_content(file_path)
    html_response = text_to_html_response(text=file_content, url=url, request=request)
    return html_response


def contains_html_tags(text: str) -> bool:
    """
     Check if text contains HTML tags or not

    :param text: text to be checked if contains HTML tag
    :returns: True if text contains HTML tags else False

    """
    pattern = re.compile(r'<.*?>')
    return bool(pattern.search(text))


def text_to_html_response(text: str, url: str = "https://abc.com", encoding: str = "utf-8", request: Request = None) -> HtmlResponse:
    """
     Converts text html to HTML object that can be parsed through xpath/css-selectors etc

    :param text: html text that to be converted to HTML response object
    :param url: URL to set in response object
    :param encoding: Encoding scheme to be applied on text
    :param request: Request object to be set in response object
    :returns: HTML response object

    """
    if not request:
        request = Request(url=url, meta={'url': url})
    return HtmlResponse(url=url, body=text, encoding=encoding, request=request)


def remove_html_from_text(text: str, parse_by_bs: bool = False) -> str:
    """
    Remove HTML tags from string & decode HTML entities e.g. (&#39; to "'")

    :param text: text to be cleaned
    :param parse_by_bs: flag to parse text using BeautifulSoup

    :returns: A cleaned text

    """
    if not text:
        return
    if parse_by_bs:
        html_parser = BeautifulSoup(text, 'html.parser')
        only_text = html_parser.get_text()
        while True:
            # Check if BeautifulSoup finds any more tags after stripping
            new_soup = BeautifulSoup(only_text, 'html.parser')
            if new_soup.find_all():
                only_text = new_soup.get_text()
                continue
            break
        cleaned_text = '\n'.join([line for line in only_text.split('\n') if line.strip() != ''])
    else:
        cleaned_text = html.unescape(text)
        cleaned_text = remove_tags(cleaned_text)
        cleaned_text = cleaned_text.strip()
    return cleaned_text


def get_proxy(proxy_provider='', proxy_user='', proxy_password='') -> dict:
    """ Create dictionary having proxy auth details"""
    proxies = {}
    try:
        if proxy_provider == 'ScraperAPI' and not proxy_user and proxy_password:
            proxy_url = f'http://scraperapi:{proxy_password}@proxy-server.scraperapi.com:8001'
            proxies = {'http': proxy_url, 'https': proxy_url}
        elif proxy_provider == 'ScraperAPI' and proxy_user and proxy_password:
            proxy_url = f'http://{proxy_user}:{proxy_password}@proxy-server.scraperapi.com:8001'
            proxies = {'http': proxy_url, 'https': proxy_url}
    except Exception as err:
        logger.error(f"Error: ({err}) at line {err.__traceback__.tb_lineno}")
    return proxies


def load_page(url, proxy_provider='', proxy_user='',
              proxy_password='', request_method='GET', headers={}, payload={}) -> object:
    """ Load webpage through requests' module & return object"""
    try:
        proxies = get_proxy(proxy_provider, proxy_user, proxy_password)
        response = requests.request(request_method, url, headers=headers,
                                    data=payload, proxies=proxies, verify=False)
        return response
    except Exception as err:
        logger.error(f"Error: ({err}) at line {err.__traceback__.tb_lineno}")


def have_attr(xpath):
    if xpath and xpath.strip('/').split('/')[-1].startswith('@'):
        return True
    else:
        return False


def parse_text(
        response: Response = None, xpath: str = None, xpaths: list = None, selector=None, _all: bool = False,
        index: int = 0, _list: bool = False, _join: str = " ", _html: bool = False, nav_child: bool = True,
        filtered_tags: tuple = ()
) -> any([str, list]):
    """
    Parse text from response object for specified xpath
    Return single text(str) or list of text(str) based on value of _list

    :param response: scrapy response object
    :param xpath: scrapy single xpath
    :param xpaths: scrapy xpaths list
    :param selector: scrapy selector object
    :param _all: flag to extract data of all xpaths
    :param index: flag to extract data of a particular index
    :param _list: flag to return data in list
    :param _join: flag to return data by joining
    :param _html: flag to check html response
    :param nav_child: flag to use nav child while extracting data
    :param filtered_tags: tags that will be removed from text along with content

    :return parsed text from the xpath(s)
    """
    all_text = []
    text = ""
    if not response and not selector:
        return
    if not xpaths and xpath:
        xpaths = [xpath]
    if not xpaths:
        return
    for xpath in xpaths:
        if not selector:
            if not _html:
                if not have_attr(xpath):
                    all_text = response.xpath(xpath + ("//text()" if nav_child else "/text()")).extract()
                else:
                    all_text = response.xpath(xpath).extract()
            else:
                html_text = response.xpath(xpath).extract()
                if filtered_tags:
                    html_text = [remove_tags_with_content(text=h, which_ones=filtered_tags) for h in html_text]
                all_text = [remove_tags(h) for h in html_text if h]
        elif selector:
            if not have_attr(xpath):
                all_text = selector.xpath(xpath + ("//text()" if nav_child else "/text()")).extract()
            else:
                all_text = selector.xpath(xpath).extract()
        if all_text:
            all_text = [t.strip() for t in all_text if t and t.strip()]
        if all_text:
            break

    if all_text:
        if all_text and index and index < len(all_text):
            text = all_text[index].strip()
        elif all_text and not _all:
            text = all_text[0]
        elif all_text and _all and not _list:
            text = f"{_join}".join(all_text)
        elif all_text and _all and _list:
            text = all_text
    return text


def parse_attr(response=None, xpath=None, xpaths=[], attr='href', selector=None, _abs=True) -> str:
    """ Parse attribute e.g. href/src from response/selector object for specified xpath"""
    if not xpaths and xpath:
        xpaths = [xpath]
    if not xpaths:
        return
    attr_value = None
    for xpath in xpaths:
        if selector and xpath:
            attr_value = selector.xpath(xpath + f"/@{attr}").extract_first()
        elif selector and not xpath:
            attr_value = selector.xpath(f"@{attr}").extract_first()
        elif response and xpath:
            attr_value = response.xpath(xpath + f"/@{attr}").extract_first()
        elif response and not xpath:
            attr_value = response.xpath(f"@{attr}").extract_first()
        else:
            attr_value = None
        if attr_value and _abs:
            attr_value = get_abs_url(response, attr_value)
        if attr_value:
            break
    return attr_value

def parse_attrs(response, xpaths, attr='href', _all=True) -> any([str, list]):
    """
    Parse attribute e.g. href/src from response object for specified xpath

    :param response: scrapy response object
    :param xpaths: scrapy xpaths list
    :param attr: attribute name

    :return parsed attribute value from the xpath(s)
    """
    selectors = get_xpath_data(response, xpaths=xpaths, _all=_all)
    attr_values = []
    for selector in selectors:
        attr_value = selector.xpath(f"@{attr}").extract_first()
        if attr_value and not _all:
            return attr_value
        elif attr_value and _all:
            attr_values.append(attr_value)
    if _all and attr_values:
        return attr_values


def get_abs_url(response, url) -> str:
    """
    Gets absolute url
    """
    base_url = response.meta.get("url") or response.request.url
    abs_url = urljoin(base_url, url)
    return abs_url


def update_graphql_api_payload(payload: dict, updated_payload_data: dict) -> dict:
    """
    Update GraphQL query payload
    """
    for key, value in updated_payload_data.items():
        payload['variables'][key] = value
    return payload


def get_url_from_response(response) -> str:
    """
    Gets request url from response
    """
    return response.meta.get('url')


def is_retry_enabled(url, status_code):
    try:
        if not status_code or not url:
            return False
        disabled_codes = [v for k, v in DISABLED_RETRY_CODES.items() if k in url]
        if disabled_codes and status_code in disabled_codes[0]:
            return False
        else:
            return True
    except Exception as err:
        logger.exception(err)


def is_retry_response(response):
    try:
        if not response:
            return True
        if response.status in RETRY_STATUS_CODES:
            return True
        else:
            return False
    except Exception as err:
        logger.exception(err)


def is_bad_response(response):
    try:
        if not response:
            return True
        if 200 <= response.status <= 300:
            return False
        else:
            return True
    except Exception as err:
        logger.exception(err)


def is_failed_request(item) -> bool:
    """
    Track if request for product is failed or not
    """
    crawl_state = item.get("crawl_state")
    if not crawl_state:
        return True
    if crawl_state not in [CrawlState.CRAWLED.value]:
        return True
    return False


def get_xpath_data(selector, xpath: str = None, xpaths: list = None, _all=True) -> list:
    """
    Gets data from xpaths.

    - It will extract data of all xpaths if _all=True
    """
    data = []
    try:
        if xpath and not xpaths:
            xpaths = [xpath]
        elif xpath and xpaths:
            xpaths.append(xpath)
        if not xpaths:
            return data

        for xpath in xpaths:
            xpath_data = selector.xpath(xpath)
            if xpath_data:
                data.extend(xpath_data)
                if not _all:
                    return data
    except:
        pass
    return data
