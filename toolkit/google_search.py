import urllib.parse

def get_google_search_url(query):
    """
    Generates a Google search URL for a given search query.

    :param query: The search query string (e.g., 'site:linkedin.com company-name').
    :returns: The complete Google search URL.
    """
    base_url = "https://www.google.com/search"
    params = {'q': query}
    query_string = urllib.parse.urlencode(params)
    return f"{base_url}?{query_string}"
