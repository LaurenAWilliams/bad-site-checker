import pytest

from bad_site_checker.app import app as flask_app


@pytest.fixture
def app():
    yield flask_app
