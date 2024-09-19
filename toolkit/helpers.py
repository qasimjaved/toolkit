def remove_substring(string, substring):
    if string and substring:
        return string.replace(substring, "").strip()
    elif not substring:
        return string


def remove_substrings(string, substrings):
    for substring in substrings:
        string = remove_substring(string, substring)
    return string

