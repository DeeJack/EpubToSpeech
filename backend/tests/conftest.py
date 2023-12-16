import pytest
from app import app as my_app

@pytest.fixture
def app():
    app = my_app
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()