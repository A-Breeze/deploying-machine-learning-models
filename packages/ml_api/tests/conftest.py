import pytest

from api.app import create_app
from api.config import TestingConfig


def pytest_configure(config):
    config.addinivalue_line(
        # Register our custom "differential" marker so it is not thrown as a warning
        # See: <https://docs.pytest.org/en/latest/mark.html#registering-marks>
        "markers", "differential: tests to compare differences between package versions"
    )

@pytest.fixture
def app():
    # noinspection PyShadowingNames
    app = create_app(config_object=TestingConfig)

    with app.app_context():
        yield app


# noinspection PyShadowingNames
@pytest.fixture
def flask_test_client(app):
    with app.test_client() as test_client:
        yield test_client
