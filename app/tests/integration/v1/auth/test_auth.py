from fastapi.testclient import TestClient


def test_user_login_success(v1_client: TestClient):
    body = {"email": "testing@test.com", "password": "testing"}

    response = v1_client.post("/auth", json=body)

    assert response.status_code == 200
    assert response.json().keys() == {"token"}


def test_user_login_unauthorized_incorrect_email(v1_client: TestClient):
    body = {"email": "incorrect@test.com", "password": "testing"}

    response = v1_client.post("/auth", json=body)

    assert response.status_code == 401
    assert response.json() == {
        "message": "You have entered an invalid email or password."
    }


def test_user_login_unauthorized_incorrect_password(v1_client: TestClient):
    body = {"email": "testing@test.com", "password": "incorrect"}

    response = v1_client.post("/auth", json=body)

    assert response.status_code == 401
    assert response.json() == {
        "message": "You have entered an invalid email or password."
    }
