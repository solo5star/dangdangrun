import json
import traceback
from datetime import datetime
from typing import Callable, Dict, List

import websockets

from .homeplus.models import Item, Store
from .state import State, state


class Client:
    host: str
    listeners: Dict[str, List[Callable]] = {}

    def __init__(self, host: str) -> None:
        self.host = host

    def _add_listener(self, event_name: str, func):
        if event_name not in self.listeners:
            self.listeners[event_name] = []

        self.listeners[event_name].append(func)

    async def _invoke_listeners(self, event_name: str, *args, **kwargs):
        if event_name not in self.listeners:
            return

        for listener in self.listeners[event_name]:
            await listener(*args, **kwargs)

    def on_update_stores(self, func):
        self._add_listener("update_stores", func)

    def on_update_items(self, func):
        self._add_listener("update_items", func)

    def on_error(self, func):
        self._add_listener("error", func)

    def on_close(self, func):
        self._add_listener("close", func)

    def on_open(self, func):
        self._add_listener("open", func)

    async def _on_receive_stores_data(self, data):
        state.update(
            State(
                stores=[Store(id=_store["id"], name=_store["name"], region=_store["region"]) for _store in data["stores"]],
            )
        )
        await self._invoke_listeners("update_stores")

    async def _on_receive_items_data(self, data):
        _items = data["items"]
        state.update(
            State(
                items=[
                    [
                        Item(
                            no=_item["no"],
                            name=_item["name"],
                            store_id=store.id,
                            stock_quantity=data["stock_quantities"][i][j],
                        )
                        for j, _item in enumerate(_items)
                    ]
                    for i, store in enumerate(state.stores)
                ],
                last_updated=datetime.fromtimestamp(data["time"] / 1000.0),
            )
        )
        await self._invoke_listeners("update_items")

    async def run(self):
        async def _on_message(message):
            response = json.loads(message)

            # parse json data and instantiate
            if response["type"] == "stores":
                await self._on_receive_stores_data(response["data"])
            elif response["type"] == "items":
                await self._on_receive_items_data(response["data"])

        async def _on_error(error):
            print("websocket client: error occured")
            print(error)
            print(traceback.format_exc())
            await self._invoke_listeners("error", error)

        async def _on_close():
            print(f"websocket client: connection closed")
            await self._invoke_listeners("close")

        async def _on_open():
            print("websocket client: connection opened")
            await self._invoke_listeners("open")

        try:
            async for websocket in websockets.connect(self.host):
                await _on_open()
                try:
                    while True:
                        message = await websocket.recv()
                        await _on_message(message)
                except websockets.ConnectionClosed as e:
                    await _on_close()
                    continue

        except Exception as e:
            await _on_error(e)
