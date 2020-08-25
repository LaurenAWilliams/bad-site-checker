import json


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    expected_response = {"text": "Hello World!"}
    assert expected_response == json.loads(response.get_data())
