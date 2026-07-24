from tests.conftest import client


def test_register_user():

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "pytest_user",
            "password": "Password123",
        },
    )

    assert response.status_code in (201, 400)


def test_login_success():

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "pytest_user",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_invalid_password():

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "pytest_user",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401

    body = response.json()

    assert body["detail"] == "Invalid username or password."