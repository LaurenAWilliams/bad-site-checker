from url_lookup_service.utils.virustotal import post_url_scan
from url_lookup_service.utils.virustotal import get_url_scan_report
from unittest.mock import patch, MagicMock


@patch('urllib.request.urlopen')
def test_post_url_scan(mock_urlopen):
    mock_resp_read = b"""
{"scan_id": "cf4b367e49bf0b22041c6f065f4aa19f3cfe39c8d5abc0617343d1a66c6a26f5-1598802494"}
    """

    mm = MagicMock()
    mm.getcode.return_value = 200
    mm.read.return_value = mock_resp_read
    mock_urlopen.return_value = mm

    expected = \
        "cf4b367e49bf0b22041c6f065f4aa19f3cfe39c8d5abc0617343d1a66c6a26f5" \
        "-1598802494", 200
    actual = post_url_scan("google.com")
    assert expected == actual
    mm.stop()


@patch('urllib.request.urlopen')
def test_get_url_scan_report(mock_urlopen):
    mock_scan_id = "cf4b367e49bf0b22041c6f065f4aa19f3cfe39c8d5abc0617343d1a66c6a26f5-1598802494"
    mock_report = b"""
{"positives": 0, "scans": {"Feodo Tracker": {"detected": false, "result": "clean site"}}}
    """

    mm = MagicMock()
    mm.getcode.return_value = 200
    mm.read.return_value = mock_report
    mock_urlopen.return_value = mm

    expected = {
                   "safe": True,
                   "details": {},
               }, 200
    actual = get_url_scan_report(mock_scan_id)
    assert expected == actual
    mm.stop()
