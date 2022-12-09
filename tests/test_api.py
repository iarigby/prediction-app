import pytest
from app.api import app as flask_app


@pytest.fixture()
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json['status'] == "available"
