import re
from typing import List, Optional, Union

from toolkit.url import parse_domain


def parse_emails(text: str, unique: bool = True, join_with: Optional[str] = None, url: Optional[str] = None) -> Union[
    List[str], str]:
    """
    Extracts all email addresses from the provided text, optionally filtering by domain from the URL.

    Args:
        text (str): The text containing email addresses.
        unique (bool): Flag to return only unique email addresses. Default is True.
        join_with (str, optional): String to join the found email addresses. If None, return as a list.
        url (str, optional): URL to filter emails by the domain. If provided, only emails matching the domain will be returned.

    Returns:
        Union[List[str], str]: A list of found email addresses or a single string if join_with is provided.
    """
    # Regular expression pattern for matching email addresses
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

    # Strip unwanted characters like \r, \n, and extra spaces from the text
    text = text.replace('\r', ' ').replace('\n', ' ').strip()

    # Find all matches in the text
    emails = re.findall(email_pattern, text)

    # Filter emails by domain if a URL is provided
    if url:
        domain = parse_domain(url)
        emails = [email for email in emails if email.split('@')[-1] == domain]

    # Get unique emails if the flag is set
    if unique:
        emails = list(set(emails))

    # Return joined string if join_with is provided, otherwise return a list
    return join_with.join(emails) if join_with else emails