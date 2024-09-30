import re
from typing import List

def parse_emails(text: str, unique: bool = True) -> List[str]:
    """
    Extracts all email addresses from the provided text.

    Args:
        text (str): The text containing email addresses.
        unique (bool): Flag to return only unique email addresses. Default is True.

    Returns:
        list: A list of found email addresses.
    """
    # Regular expression pattern for matching email addresses
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

    # Find all matches in the text
    emails = re.findall(email_pattern, text)

    # Return unique emails if the flag is set
    return list(set(emails)) if unique else emails