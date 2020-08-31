import urllib.request
import validators

def is_url_reachable(url):
    req = urllib.request.Request(url=url, method="HEAD")
    try:
        urllib.request.urlopen(req, timeout=1)
        return True
    except urllib.request.HTTPError:
        return False

def is_url_valid(url):
    return validators.url(url)