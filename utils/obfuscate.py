def html_obfuscate_string(string):
    """Obfuscates a string by converting it to HTML entities

    Useful for obfuscating an email address to prevent being crawled by spambots
    """
    obfuscated = ''.join(['&#%s;' % str(ord(char)) for char in string])
    return obfuscated
