import json
from unittest.mock import patch, MagicMock


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    expected_response = {"text": "Hello World!"}
    assert expected_response == json.loads(response.get_data())

@patch('url_lookup_service.utils.virustotal')
def test_url_lookup(mock_virustotal, client):
    response = client.get('/urlinfo/1/auctionbowling.com')
    mm = MagicMock()
    mm.post_url_scan.return_value = "22", 200
    mm.get_url_scan_report.return_value = {"safe": False, "details": {
        "AutoShun": "malicious site"}}, 200
    mock_virustotal.return_value = mm

    assert response.status_code == 200
    expected_response = {
        "details": {
            "AutoShun": "malicious site"
        },
        "lookup_url": "auctionbowling.com",
        "safe": False
    }
    assert expected_response == json.loads(response.get_data())
