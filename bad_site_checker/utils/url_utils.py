"""
Utility to verify URLs
"""
import urllib.error
import urllib.request

import validators


def is_url_reachable(url):
    """
    Use HEAD method to check URL is reachable without downloading contents
    :param url: url we are checking
    :return: True if reachable, False if not
    """
    req = urllib.request.Request(url=url, method="HEAD")
    try:
        urllib.request.urlopen(req, timeout=3)
        return True
    except urllib.error.URLError:
        return False


def is_url_valid(url):
    """
    Use validators to check url against url regex
    :param url: url we are checking
    :return: True if valid, False if not
    """
    return validators.url(url)
