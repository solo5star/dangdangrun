from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Deque, List

from .homeplus.models import Item, StockChange, Store


@dataclass
class State:
    stores: List[Store] = None
    previous_items: List[List[Item]] = None
    items: List[List[Item]] = None
    last_updated: datetime = None
    stock_changes: Deque[StockChange] = field(default_factory=deque)

    @property
    def regions(self) -> List[str]:
        return list(dict.fromkeys(store.region for store in self.stores))

    def update(self, next_state: "State"):
        if next_state.stores is not None:
            # stores changed? reset all data
            if self.stores is None or any(map(lambda t: t[0].id != t[1].id, zip(self.stores, next_state.stores))):
                self.previous_items = None
                self.items = None
                self.last_updated = None

            self.stores = next_state.stores

        if next_state.items is not None:
            self.previous_items = self.items
            self.items = next_state.items
            self.last_updated = next_state.last_updated or datetime.now()

            # check difference of stock quantity,
            # and logging it
            if self.previous_items is not None:
                for i, store in enumerate(self.stores):
                    for j, items_in_store in enumerate(self.items[i]):
                        item = self.items[i][j]
                        previous_item = self.previous_items[i][j]

                        if previous_item.stock_quantity != item.stock_quantity:
                            self.stock_changes.append(
                                StockChange(
                                    time=self.last_updated,
                                    store=store,
                                    item=item,
                                    previous=previous_item.stock_quantity,
                                    current=item.stock_quantity,
                                )
                            )
                            # keep stock_changes size 1000
                            if len(self.stock_changes) > 1000:
                                self.stock_changes.popleft()


state = State()
