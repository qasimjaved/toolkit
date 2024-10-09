def strip_special_characters(text: str) -> str:
    """
    Strips special characters (like commas) from the sides of the provided text,
    but keeps them inside the text intact.

    :param text: The input text containing special characters.

    :returns: The text with special characters stripped from the sides.
    """
    return text.strip(",.?!@#$%^&*()_+=-[]{}|;:\"'<>/\\`~").strip()
