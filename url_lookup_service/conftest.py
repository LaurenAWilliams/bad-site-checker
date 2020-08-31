import pytest

from url_lookup_service.app import app as flask_app


@pytest.fixture
def app():
    yield flask_app
