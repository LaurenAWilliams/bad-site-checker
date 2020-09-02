import urllib.error
from unittest.mock import patch, MagicMock

from url_lookup_service.utils.url_utils import is_url_valid, is_url_reachable


def test_bad_url_valid():
    url = "thisisabadurl"
    returned = is_url_valid(url)
    assert not returned


def test_good_url_valid():
    url = "https://www.google.com"
    returned = is_url_valid(url)
    assert returned


@patch('urllib.request')
@patch('urllib.request.urlopen')
def test_url_unreachable(mock_urlopen, mock_request):
    def _raise_urlerror():
        raise urllib.error.URLError(reason="Testing")

    mm = MagicMock()
    mm.raiseError.side_effect = _raise_urlerror
    mock_urlopen.return_value = mm

    expected = False
    actual = is_url_reachable("https://www.unreachableurl.com")
    assert expected == actual
    mm.stop()


@patch('urllib.request')
@patch('urllib.request.urlopen')
def test_url_unreachable(mock_urlopen, mock_request):
    mm = MagicMock()
    mock_urlopen.return_value = mm

    expected = True
    actual = is_url_reachable("https://www.reachableurl.com")
    assert expected == actual
    mm.stop()
