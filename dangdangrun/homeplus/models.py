from dataclasses import dataclass
from datetime import datetime


@dataclass
class Store:
    id: int
    name: str
    region: str


@dataclass
class Item:
    no: str
    name: str
    store_id: int
    stock_quantity: int


@dataclass
class StockChange:
    time: datetime
    store: Store
    item: Item
    previous: int
    current: int
