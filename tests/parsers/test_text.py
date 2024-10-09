import pytest
from toolkit.parsers.text import parse_emails  # Replace 'your_module' with the actual module name where the function resides


@pytest.mark.parametrize("text, unique, join_with, url, expected", [
    # Basic email extraction
    ("Contact us at email@example.com", True, None, None, ["email@example.com"]),

    # Multiple emails extraction
    ("Emails: first@example.com, second@example.com", True, None, None, ["first@example.com", "second@example.com"]),

    # No email in the text
    ("No email here", True, None, None, []),

    # Duplicate emails with unique=True
    ("Duplicate emails: test@example.com, test@example.com", True, None, None, ["test@example.com"]),

    # Duplicate emails with unique=False
    ("Duplicate emails: test@example.com, test@example.com", False, None, None,
     ["test@example.com", "test@example.com"]),

    # Email extraction with join_with parameter
    ("email1@example.com, email2@example.com", True, ", ", None, "email1@example.com, email2@example.com"),

    # Email extraction with join_with parameter along with "." in emails
    ("user1@example.com., user2@another.com", True, None, "http://example.com", ["user1@example.com"]),

    # Filter emails by domain
    ("user1@example.com, user2@another.com", True, None, "http://example.com", ["user1@example.com"]),

    # Strip unwanted characters in the text
    (" \nemail@example.com\r ", True, None, None, ["email@example.com"]),

    # Empty text
    ("", True, None, None, []),

    # Text with no emails
    ("This text has no emails", True, None, None, []),
])
def test_parse_emails(text, unique, join_with, url, expected):
    # Call the parse_emails function with the parameters
    result = parse_emails(text, unique=unique, join_with=join_with, url=url)

    # Assert the expected result
    assert result == expected