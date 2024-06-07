"""
Collection of validators used in aegis_scan
"""
import re


# Function to validate URL
def validate_url(url: str) -> bool:
    """
    Validte URL
    """
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    
    regex_compiled = re.compile(regex)

    if str is None or '':
        return False
    
    if re.search(regex_compiled, url):
        return True
    else:
        return False
