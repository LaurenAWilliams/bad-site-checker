import urllib.request
import urllib.error
import validators


def is_url_reachable(url):
    req = urllib.request.Request(url=url, method="HEAD")
    try:
        urllib.request.urlopen(req, timeout=3)
        return True
    except urllib.error.URLError:
        return False


def is_url_valid(url):
    return validators.url(url)
