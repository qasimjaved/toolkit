from urllib.parse import urlparse


def is_about_page(url: str) -> bool:
    """
    Check if the given URL is likely an "About Us" page.

    :param url: The URL to check.

    :return: True if the URL suggests it's an "About Us" page, False otherwise.
    """
    # Normalize URL and extract path
    path = urlparse(url).path.lower()
    about_keywords = ['about', 'about-us', 'about-us/', 'who-we-are', 'team', 'our-team']
    return any(keyword in path for keyword in about_keywords)


def is_contact_page(url: str) -> bool:
    """
    Check if the given URL is likely a "Contact Us" page.

    :param url: The URL to check.

    :return: True if the URL suggests it's a "Contact Us" page, False otherwise.
    """
    # Normalize URL and extract path
    parsed_url = urlparse(url)
    path = parsed_url.path.lower()

    # Define keywords that indicate a contact page
    contact_keywords = ['contact', 'contact-us', 'get-in-touch', 'reach-us']

    # Define file extensions to exclude
    excluded_extensions = ['.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.pdf', '.svg']

    # Check if the path contains any excluded extensions
    if any(path.endswith(ext) for ext in excluded_extensions):
        return False

    # Check if the path contains any contact keywords
    return any(keyword in path for keyword in contact_keywords)


def is_about_or_contact_page(url: str) -> bool:
    """
    Check if the given URL is likely an "About Us" or "Contact Us" page.

    :param url: The URL to check.

    :return: True if the URL suggests it's an "About Us" or "Contact Us" page, False otherwise.
    """
    # Normalize URL and extract path
    return  is_about_page(url) or is_contact_page(url)