from fastapi.testclient import TestClient
from listas_service.main import app

client = TestClient(app)


def test_list_lists():
    resp = client.get("/lists")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_create_list():
    new_list = {
        "name": "Compra rápida",
        "items": [
            {"product_id": 1, "quantity": 1}
        ]
    }
    resp = client.post("/lists", json=new_list)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Compra rápida"
    assert len(data["items"]) == 1
