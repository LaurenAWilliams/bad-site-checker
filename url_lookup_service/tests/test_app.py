import json
from pytest_mock import mock


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    expected_response = {"text": "Hello World!"}
    assert expected_response == json.loads(response.get_data())

@mock.patch('url_lookup_service.app.post_url_scan')
@mock.patch('url_lookup_service.app.get_url_scan_report')
def test_url_lookup(mock_get_url_scan_report, mock_post_url_scan, client):

    mock_post_url_scan.return_value = 20000, 200
    mock_get_url_scan_report.return_value = {
        "safe": False,
        "details": {
            "AutoShun": "malicious site"
        }
    }, 200
    response = client.get('/urlinfo/1/auctionbowling.com')

    assert response.status_code == 200
    expected_response = {
        "details": {
            "AutoShun": "malicious site"
        },
        "lookup_url": "auctionbowling.com",
        "safe": False
    }
    assert expected_response == json.loads(response.get_data())
