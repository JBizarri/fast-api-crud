from typing import Any, Dict
from uuid import uuid4

from fastapi.testclient import TestClient


def test_read_companies_success(v1_client: TestClient, testing_token: str):
    headers = {"authorization": f"Bearer {testing_token}"}

    response = v1_client.get("/companies", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_read_companies_unauthorizaed(v1_client: TestClient):
    response = v1_client.get("/companies")
    assert response.status_code == 401


def test_create_company_success(v1_client: TestClient, testing_token: str):
    headers = {"authorization": f"Bearer {testing_token}"}
    body = {"name": "Company"}

    response = v1_client.post("/companies", headers=headers, json=body)

    assert response.status_code == 200
    company: Dict[str, Any] = response.json()
    assert company.keys() == {"id", "name"}
    assert company["name"] == "Company"


def test_create_company_unauthorizaed(v1_client: TestClient):
    body = {"name": "Company"}
    response = v1_client.post("/companies", json=body)
    assert response.status_code == 401


def test_create_company_unprocessable_entity_invalid_name(
    v1_client: TestClient, testing_token: str
):
    headers = {"authorization": f"Bearer {testing_token}"}
    body = {"name": " "}

    response = v1_client.post("/companies", headers=headers, json=body)

    assert response.status_code == 422
    assert response.json() == {"message": "Invalid name, please try another."}


def test_read_company_success(v1_client: TestClient, testing_token: str):
    # Create a company
    headers = {"authorization": f"Bearer {testing_token}"}
    post_body = {"name": "Company"}

    post_company = v1_client.post("/companies", headers=headers, json=post_body).json()

    # Read created company
    response = v1_client.get(f"/companies/{post_company['id']}", headers=headers)

    assert response.status_code == 200
    get_company: Dict[str, Any] = response.json()
    assert get_company["id"] == post_company["id"]
    assert get_company["name"] == post_body["name"]


def test_read_company_unauthorized(v1_client: TestClient):
    response = v1_client.get(f"/companies/{uuid4()}")
    assert response.status_code == 401


def test_read_company_not_found(v1_client: TestClient, testing_token: str):
    headers = {"authorization": f"Bearer {testing_token}"}
    response = v1_client.get(f"/companies/{uuid4()}", headers=headers)

    assert response.status_code == 404
    assert response.json() == {"message": "Company was not found."}


def test_update_company_success(v1_client: TestClient, testing_token: str):
    # Create a company
    headers = {"authorization": f"Bearer {testing_token}"}
    post_body = {"name": "Company"}

    post_company = v1_client.post("/companies", headers=headers, json=post_body).json()

    put_body = {"name": "New company name"}
    response = v1_client.put(
        f"/companies/{post_company['id']}", headers=headers, json=put_body
    )

    assert response.status_code == 200
    put_company = response.json()
    assert put_company["id"] == post_company["id"]
    assert put_company["name"] == "New company name"


def test_update_company_unauthorized(v1_client: TestClient):
    response = v1_client.put(f"/companies/{uuid4()}")
    assert response.status_code == 401


def test_update_company_not_found(v1_client: TestClient, testing_token: str):
    headers = {"authorization": f"Bearer {testing_token}"}
    put_body = {"name": "New company name"}

    response = v1_client.put(f"/companies/{uuid4()}", headers=headers, json=put_body)

    assert response.status_code == 404
    assert response.json() == {"message": "Company was not found."}


def test_update_company_unprocessable_entity_invalid_name(
    v1_client: TestClient, testing_token: str
):
    # Create a company
    headers = {"authorization": f"Bearer {testing_token}"}
    post_body = {"name": "Company"}

    post_company = v1_client.post("/companies", headers=headers, json=post_body).json()

    put_body = {"name": ""}
    response = v1_client.put(
        f"/companies/{post_company['id']}", headers=headers, json=put_body
    )

    assert response.status_code == 422
    assert response.json() == {"message": "Invalid name, please try another."}


def test_delete_company_success(v1_client: TestClient, testing_token: str):
    # Create a company
    headers = {"authorization": f"Bearer {testing_token}"}
    post_body = {"name": "Company"}

    post_company = v1_client.post("/companies", headers=headers, json=post_body).json()

    response = v1_client.delete(f"/companies/{post_company['id']}", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "OK"}

    response = v1_client.get(f"/companies/{post_company['id']}", headers=headers)
    assert response.status_code == 404


def test_delete_company_unauthorized(v1_client: TestClient):
    response = v1_client.delete(f"/companies/{uuid4()}")
    assert response.status_code == 401


def test_delete_company_not_found(v1_client: TestClient, testing_token: str):
    headers = {"authorization": f"Bearer {testing_token}"}
    response = v1_client.delete(f"/companies/{uuid4()}", headers=headers)

    assert response.status_code == 404
    assert response.json() == {"message": "Company was not found."}
