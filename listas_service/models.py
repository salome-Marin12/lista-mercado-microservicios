from pydantic import BaseModel
from typing import List, Optional


class ListItem(BaseModel):
    product_id: int
    quantity: int


class ShoppingListBase(BaseModel):
    name: str
    items: List[ListItem]


class ShoppingListCreate(ShoppingListBase):
    pass


class ShoppingList(ShoppingListBase):
    id: int


class ShoppingListUpdate(BaseModel):
    name: Optional[str] = None
    items: Optional[List[ListItem]] = None


class ProductDetail(BaseModel):
    id: int
    name: str
    category: str
    price: float


class ListItemDetail(BaseModel):
    product: ProductDetail
    quantity: int
    subtotal: float


class ShoppingListDetails(BaseModel):
    id: int
    name: str
    items: List[ListItemDetail]
    total: float
