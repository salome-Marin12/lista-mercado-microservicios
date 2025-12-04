from fastapi import FastAPI, HTTPException
from typing import List
from models import Product, ProductCreate, ProductUpdate

app = FastAPI(
    title="Productos Service",
    description="Microservicio para gestionar el catálogo de productos de la lista de mercado",
    version="1.0.0"
)

# "Base de datos" en memoria
products_db: dict[int, Product] = {}
current_id = 0


def get_next_id() -> int:
    global current_id
    current_id += 1
    return current_id


# Datos iniciales
def seed_data():
    if products_db:
        return
    p1 = Product(id=get_next_id(), name="Leche", category="Lácteos", price=4500)
    p2 = Product(id=get_next_id(), name="Pan", category="Panadería", price=2500)
    p3 = Product(id=get_next_id(), name="Huevos", category="Huevos", price=17000)
    products_db[p1.id] = p1
    products_db[p2.id] = p2
    products_db[p3.id] = p3


seed_data()


@app.get("/products", response_model=List[Product])
def list_products():
    return list(products_db.values())


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@app.post("/products", response_model=Product, status_code=201)
def create_product(data: ProductCreate):
    new_id = get_next_id()
    product = Product(id=new_id, **data.model_dict())
    products_db[new_id] = product
    return product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, data: ProductUpdate):
    existing = products_db.get(product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    updated_data = existing.model_dict()
    for field, value in data.model_dict(exclude_unset=True).items():
        updated_data[field] = value

    updated_product = Product(**updated_data)
    products_db[product_id] = updated_product
    return updated_product


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    del products_db[product_id]
    return
