from fastapi import FastAPI, HTTPException
from typing import List
import httpx
import os


from models import (
    ShoppingList, ShoppingListCreate, ShoppingListUpdate,
    ShoppingListDetails, ListItemDetail, ProductDetail
)

app = FastAPI(
    title="Listas Service",
    description="Microservicio para gestionar listas de mercado",
    version="1.0.0"
)

# URL del microservicio de productos
PRODUCTS_SERVICE_URL_LOCAL = "http://localhost:8001"


# "Base de datos" en memoria
lists_db: dict[int, ShoppingList] = {}
current_id = 0


def get_next_id() -> int:
    global current_id
    current_id += 1
    return current_id


def seed_data():
    if lists_db:
        return
    l1 = ShoppingList(
        id=get_next_id(),
        name="Compra quincenal",
        items=[
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 1}
        ]
    )
    lists_db[l1.id] = l1


seed_data()


@app.get("/lists", response_model=List[ShoppingList])
def list_lists():
    return list(lists_db.values())


@app.get("/lists/{list_id}", response_model=ShoppingList)
def get_list(list_id: int):
    lista = lists_db.get(list_id)
    if not lista:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    return lista


@app.post("/lists", response_model=ShoppingList, status_code=201)
def create_list(data: ShoppingListCreate):
    new_id = get_next_id()
    lista = ShoppingList(id=new_id, **data.model_dict())
    lists_db[new_id] = lista
    return lista


@app.put("/lists/{list_id}", response_model=ShoppingList)
def update_list(list_id: int, data: ShoppingListUpdate):
    existing = lists_db.get(list_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Lista no encontrada")

    updated_data = existing.model_dict()
    for field, value in data.model_dict(exclude_unset=True).items():
        updated_data[field] = value

    updated_list = ShoppingList(**updated_data)
    lists_db[list_id] = updated_list
    return updated_list


@app.delete("/lists/{list_id}", status_code=204)
def delete_list(list_id: int):
    if list_id not in lists_db:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    del lists_db[list_id]
    return


@app.get("/lists/{list_id}/details", response_model=ShoppingListDetails)
async def get_list_details(list_id: int):
    """
    Devuelve la lista con detalle de productos.
    Usa el microservicio de productos que corre en localhost:8001
    """
    lista = lists_db.get(list_id)
    if not lista:
        raise HTTPExcepti

