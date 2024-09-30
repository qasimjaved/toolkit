from typing import List, Optional, Union
from scrapy.http import Response

def parse_text(response: Optional[Response], xpaths: Optional[List[str]] = None,
               extract_all: bool = False, index: int = 0,
               return_list: bool = False, join_with: str = " ",
               return_html: bool = False, nav_child: bool = True,
               filtered_tags: tuple = ()) -> Union[str, List[str]]:
    """
    Parse text from response object for specified xpaths.

    :param response: Scrapy response object.
    :param xpaths: List of xpath expressions (if None, extract all text).
    :param extract_all: Flag to extract data from all xpaths.
    :param index: Index to extract data from.
    :param return_list: Flag to return data as a list.
    :param join_with: String to join results.
    :param return_html: Flag to check HTML response.
    :param nav_child: Flag to use nav child while extracting data.
    :param filtered_tags: Tags to be removed from text along with their content.

    :return: Parsed text from the xpath(s) or all text if no xpaths provided.
    """
    if not response:
        return []

    if xpaths is None:
        # If no xpaths are specified, extract all text from the response
        return _extract_all_text(response, nav_child, return_html, filtered_tags)

    all_text = []
    for xpath in xpaths:
        extracted_text = _extract_text_with_response(response, xpath, nav_child, return_html, filtered_tags)
        all_text.extend([t.strip() for t in extracted_text if t.strip()])

    return _process_extracted_text(all_text, extract_all, index, return_list, join_with)

def _extract_all_text(response: Response, nav_child: bool, return_html: bool, filtered_tags: tuple) -> List[str]:
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
                             return_list: bool, join_with: str) -> Union[str, List[str]]:
    """
    Process the extracted text based on the provided flags.

    :param all_text: List of extracted text.
    :param extract_all: Flag to extract all texts.
    :param index: Index to return specific text.
    :param return_list: Flag to return as list.
    :param join_with: String to join the text if returning all.

    :return: Processed text as string or list.
    """
    if not all_text:
        return []

    if extract_all:
        return all_text if return_list else join_with.join(all_text)

    return all_text[index].strip() if index < len(all_text) else all_text[0]
