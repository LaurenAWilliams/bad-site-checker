import json

from pytest_mock import mock


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    expected_response = {"text": "Hello World!"}
    assert expected_response == json.loads(response.get_data())


@mock.patch('bad_site_checker.app.Database')
@mock.patch('bad_site_checker.app.is_url_valid')
@mock.patch('bad_site_checker.app.is_url_reachable')
@mock.patch('bad_site_checker.app.post_url_scan')
@mock.patch('bad_site_checker.app.get_url_scan_report')
def test_url_lookup_no_existing_data(mock_get_url_scan_report, mock_post_url_scan,
                                     mock_is_url_reachable, mock_is_url_valid, mock_db,
                                     client):
    mock_db_class = mock_db.return_value
    mock_db_class.fetch_by_url.return_value = None
    mock_is_url_valid.return_value = True
    mock_is_url_reachable.return_value = True
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


@mock.patch('bad_site_checker.app.Database')
@mock.patch('bad_site_checker.app.is_url_valid')
@mock.patch('bad_site_checker.app.is_url_reachable')
def test_url_lookup_existing_data(mock_is_url_reachable, mock_is_url_valid, mock_db, client):
    data = {"safe": False, "details": '{"AutoShun": "malicious site"}', "url": "auctionbowling.com"}
    mock_db_class = mock_db.return_value
    mock_db_class.fetch_by_url.return_value = data
    mock_is_url_valid.return_value = True
    mock_is_url_reachable.return_value = True

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


@mock.patch('bad_site_checker.app.Database')
@mock.patch('bad_site_checker.app.is_url_valid')
@mock.patch('bad_site_checker.app.is_url_reachable')
@mock.patch('bad_site_checker.app.post_url_scan')
def test_url_lookup_204_from_vt(mock_post_url_scan, mock_is_url_reachable, mock_is_url_valid, mock_db, client):
    mock_db_class = mock_db.return_value
    mock_db_class.fetch_by_url.return_value = None
    mock_is_url_valid.return_value = True
    mock_is_url_reachable.return_value = True
    mock_post_url_scan.return_value = None, 204
    response = client.get('/urlinfo/1/auctionbowling.com')

    assert response.status_code == 500
    expected_response = {'reason': 'server error, got 204 from internal apis'}
    assert expected_response == json.loads(response.get_data())
