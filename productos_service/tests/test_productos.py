from fastapi.testclient import TestClient
from productos_service.main import app

client = TestClient(app)


def test_list_products():
    resp = client.get("/products")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_create_product():
    new_product = {
        "name": "Arroz",
        "category": "Granos",
        "price": 5200
    }
    resp = client.post("/products", json=new_product)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] is not None
    assert data["name"] == "Arroz"
