from w3lib.html import remove_tags, remove_tags_with_content
from scrapy.http import Request, HtmlResponse
from bs4 import BeautifulSoup
import html
from scrapy.http import Response

from typing import List, Optional, Union


def text_to_html_response(text: str, url: str = "https://abc.com", encoding: str = "utf-8",
                          request: Optional[Request] = None) -> HtmlResponse:
    """
    Converts text HTML to an HTML object that can be parsed through XPath/CSS selectors.

    :param text: HTML text to be converted to an HTML response object.
    :param url: URL to set in the response object.
    :param encoding: Encoding scheme to be applied to the text.
    :param request: Request object to be set in the response object.

    :returns: HTML response object.
    """
    request = request or Request(url=url, meta={'url': url})
    return HtmlResponse(url=url, body=text, encoding=encoding, request=request)

def remove_html_from_text(text: str, parse_with_bs: bool = False) -> str:
    """
    Remove HTML tags from string and decode HTML entities (e.g. &#39; to "'").

    :param text: Text to be cleaned.
    :param parse_with_bs: Flag to parse text using BeautifulSoup.

    :returns: A cleaned text.
    """
    if not text:
        return ""
    return _clean_text_with_bs(text) if parse_with_bs else _clean_text_without_bs(text)

def _clean_text_with_bs(text: str) -> str:
    """
    Clean text using BeautifulSoup to remove HTML tags.

    :param text: HTML text to be cleaned.

    :return: Cleaned text.
    """
    cleaned_text = BeautifulSoup(text, 'html.parser').get_text()
    while True:
        new_soup = BeautifulSoup(cleaned_text, 'html.parser')
        if new_soup.find_all():
            cleaned_text = new_soup.get_text()
        else:
            break

    return '\n'.join(line for line in cleaned_text.split('\n') if line.strip())

def _clean_text_without_bs(text: str) -> str:
    """
    Clean text without using BeautifulSoup.

    :param text: HTML text to be cleaned.

    :return: Cleaned text.
    """
    cleaned_text = html.unescape(text)
    return cleaned_text.strip()  # Assuming remove_tags function is defined elsewhere


def _extract_text_with_response(response: Response, xpath: str, nav_child: bool,
                                return_html: bool, filtered_tags: tuple) -> List[str]:
    """
    Extract text using a Scrapy response.

    :param response: Scrapy response object.
    :param xpath: XPath expression to extract text from.
    :param nav_child: Flag to navigate child nodes.
    :param return_html: Flag to indicate if HTML response should be processed.
    :param filtered_tags: Tags to remove from the HTML.

    :return: Extracted text as a list.
    """
    if not return_html:
        return response.xpath(xpath + ("//text()" if nav_child else "/text()")).extract()

    html_text = response.xpath(xpath).extract()
    if filtered_tags:
        html_text = [remove_tags_with_content(text=h, which_ones=filtered_tags) for h in html_text]
    return [remove_tags(h) for h in html_text if h]


def parse_text(response: Optional[Response], xpaths: Optional[List[str]] = (),
               extract_all: bool = False, index: int = 0,
               join_with: str = None,
               return_html: bool = False, nav_child: bool = True,
               filtered_tags: tuple = ()) -> Union[str, List[str]]:
    """
    Parse text from response object for specified xpaths.

    :param response: Scrapy response object.
    :param xpaths: List of xpath expressions (if None, extract all text).
    :param extract_all: Flag to extract data from all xpaths.
    :param index: Index to extract data from.
    :param join_with: String to join results.
    :param return_html: Flag to check HTML response.
    :param nav_child: Flag to use nav child while extracting data.
    :param filtered_tags: Tags to be removed from text along with their content.

    :return: Parsed text from the xpath(s) or all text if no xpaths provided.
    """
    if not response:
        return []

    all_text = []

    if not xpaths:
        # If no xpaths are specified, extract all text from the response
        all_text = _extract_all_text(response, nav_child, filtered_tags)
    else:
        for xpath in xpaths:
            all_text = _extract_text_with_response(response, xpath, nav_child, return_html, filtered_tags)

    return _process_extracted_text(all_text, extract_all, index, join_with)

def _extract_all_text(response: Response, nav_child: bool, filtered_tags: tuple) -> List[str]:
    """
    Extract all text from the response.

    :param response: Scrapy response object.
    :param nav_child: Flag to navigate child nodes.
    :param return_html: Flag to indicate if HTML response should be processed.
    :param filtered_tags: Tags to remove from the HTML.

    :return: List of all extracted text.
    """
    # Use XPath to get all text nodes from the document
    xpath_expression = "//text()" if nav_child else "/text()"
    all_text = response.xpath(xpath_expression).extract()

    # Filter out unwanted tags if specified
    if filtered_tags:
        all_text = [remove_tags_with_content(text=h, which_ones=filtered_tags) for h in all_text]

    return [remove_tags(h) for h in all_text if h]



def _process_extracted_text(all_text: List[str], extract_all: bool, index: int,
                            join_with: str) -> Union[str, List[str]]:
    """
    Process the extracted text based on the provided flags.

    :param all_text: List of extracted text.
    :param extract_all: Flag to extract all texts.
    :param index: Index to return specific text.
    :param join_with: String to join the text if returning all.

    :return: Processed text as string or list.
    """
    all_text = [t.strip() for t in all_text if t.strip()]

    if not all_text:
        return []

    if extract_all:
        return all_text if not join_with else join_with.join(all_text)

    return all_text[index].strip() if index < len(all_text) else all_text[0]
