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


def test_predict_endpoint_malignant(client):
    prediction_request_body = {'texture_mean': 17.77, 'area_mean': 1326.0, 'concavity_mean': 0.0869, 'area_se': 74.08,
                               'concavity_se': 0.0186, 'fractal_dimension_se': 0.003532, 'smoothness_worst': 0.1238,
                               'concavity_worst': 0.2416, 'symmetry_worst': 0.275, 'fractal_dimension_worst': 0.08902}
    response = client.get("/predict", json=prediction_request_body)
    assert response.status_code == 200
    assert response.json['prediction'] == 1


def test_predict_endpoint_benign(client):
    prediction_request_body = {'texture_mean': 14.36, 'area_mean': 566.3, 'concavity_mean': 0.06664, 'area_se': 23.56,
                               'concavity_se': 0.02387, 'fractal_dimension_se': 0.0023, 'smoothness_worst': 0.144,
                               'concavity_worst': 0.239, 'symmetry_worst': 0.2977, 'fractal_dimension_worst': 0.07259}
    response = client.get("/predict", json=prediction_request_body)
    assert response.status_code == 200
    assert response.json['prediction'] == 0


def test_predict_endpoint_attribute_checking(client):
    prediction_request_body = {'texture_mean': 14.36}
    response = client.get("/predict", json=prediction_request_body)
    assert response.status_code == 422
    assert response.json['error'] == 'one or more important values missing from data'
