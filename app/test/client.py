import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def authenticate_user(client):
    response = client.post("api/dev/token",
                           data={"username": "admin",
                                 "password": "secret"})
    return response.json()["access_token"]


def test_create_booking(client):
    token = authenticate_user(client)

    headers = {"Authorization": f"Bearer {token}"}
    booking_request = {
        "check_in_date": "2023-10-10",
        "check_out_date": "2023-10-15",
        "room_number": 101,
        "purpose": "Business"
    }

    response = client.post("api/dev/booking", json=booking_request, headers=headers)

    assert response.status_code == 201
    assert "createdId" in response.json()
