import pytest
from toolkit.cleaning import strip_special_characters  # Replace 'your_module' with the actual module name where the function resides

@pytest.mark.parametrize("input_text, expected", [
    ("Hello, World!", "Hello, World"),          # Commas inside remain
    (",Test,", "Test"),                         # Comma stripped from both sides
    (" Special test. ", "Special test"),        # Space trimmed and special character removed
    ("##Hello!!", "Hello"),                     # Special characters from both sides
    ("--Test--", "Test"),                       # Hyphens stripped from sides
    ("No special characters", "No special characters"),  # No change when no special characters on the side
    ("", ""),                                   # Empty input
])
def test_strip_special_characters(input_text, expected):
    assert strip_special_characters(input_text) == expected
