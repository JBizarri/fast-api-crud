from . import v2_client


def test_root():
    response = v2_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}
