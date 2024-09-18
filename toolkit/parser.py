import re


def parse_emails(text):
    """
    Extracts all email addresses from the provided text.

    Args:
        text (str): The text containing email addresses.

    Returns:
        list: A list of found email addresses.
    """
    # Regular expression pattern for matching email addresses
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

    # Find all matches in the text
    emails = re.findall(email_pattern, text)

    return emails
