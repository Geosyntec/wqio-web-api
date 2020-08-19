# from flask import json
import json
from flask import jsonify

import pytest
import numpy.testing as nptest


from application import app

DEV_URL = "http://127.0.0.1:5000"
PROD_URL = "https://wqros.azurewebsites.net"

as_array_data = {
    "values": [
        5.0,
        5.0,
        5.5,
        5.75,
        9.5,
        9.5,
        11.0,
        2.0,
        4.2,
        4.62,
        5.57,
        5.66,
        5.86,
        6.65,
        6.78,
        6.79,
        7.5,
        7.5,
        7.5,
        8.63,
        8.71,
        8.99,
        9.85,
        10.82,
        11.25,
        11.25,
        12.2,
        14.92,
        16.77,
        17.81,
        19.16,
        19.19,
        19.64,
        20.18,
        22.97,
    ],
    "censored": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
}

as_parts_data = {
    "censored": [5.0, 5.0, 5.5, 5.75, 9.5, 9.5, 11.0],
    "uncensored": [
        2.0,
        4.2,
        4.62,
        5.57,
        5.66,
        5.86,
        6.65,
        6.78,
        6.79,
        7.5,
        7.5,
        7.5,
        8.63,
        8.71,
        8.99,
        9.85,
        10.82,
        11.25,
        11.25,
        12.2,
        14.92,
        16.77,
        17.81,
        19.16,
        19.19,
        19.64,
        20.18,
        22.97,
    ],
}


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def expected():
    return [
        3.11,
        3.61,
        4.05,
        4.05,
        4.71,
        6.14,
        6.98,
        2.00,
        4.20,
        4.62,
        5.57,
        5.66,
        5.86,
        6.65,
        6.78,
        6.79,
        7.50,
        7.50,
        7.50,
        8.63,
        8.71,
        8.99,
        9.85,
        10.82,
        11.25,
        11.25,
        12.20,
        14.92,
        16.77,
        17.81,
        19.16,
        19.19,
        19.64,
        20.18,
        22.97,
    ]


def test_add():
    response = app.test_client().post(
        "/v1/add", data=json.dumps({"a": 1, "b": 2}), content_type="application/json",
    )

    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["sum"] == 3


def test_echo(client):
    response = client.get("/echo")
    assert response.status_code == 200
    assert response.content_type == "application/json"


@pytest.mark.parametrize(
    ("endpoint", "data"),
    [("/v1/as_arrays", as_array_data), ("/v1/as_parts", as_parts_data),],
)
def test_ros_endpoints(endpoint, data, expected, client):
    response = client.post(endpoint, json=data)
    assert response.status_code == 200
    result = json.loads(response.get_data(as_text=True))
    nptest.assert_almost_equal(result, expected, decimal=2)
