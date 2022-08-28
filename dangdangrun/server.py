import asyncio
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.responses import FileResponse

from . import settings
from .homeplus.constants import get_stores_in_region
from .state import state

app = FastAPI()
connections: List[WebSocket] = []


state.stores = get_stores_in_region(settings.REGIONS)


@app.on_event("startup")
def on_startup():
    from .tasks import scheduler

    scheduler.start()


@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.get("/debug")
async def debug():
    return FileResponse("static/debug.html")


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    await broadcast_stores()
    await broadcast_items()

    try:
        while True:
            await websocket.receive_bytes()
    except WebSocketDisconnect:
        pass

    connections.remove(websocket)


async def broadcast_json(data):
    await asyncio.gather(*[connection.send_json(data) for connection in connections])


async def broadcast_stores():
    await broadcast_json(
        {
            "type": "stores",
            "data": {"stores": [{"id": store.id, "name": store.name, "region": store.region} for store in state.stores]},
        }
    )


async def broadcast_items():
    if state.items is None or state.last_updated is None:
        return

    await broadcast_json(
        {
            "type": "items",
            "data": {
                "time": int(state.last_updated.timestamp() * 1000),
                "items": [
                    {
                        "no": item.no,
                        "name": item.name,
                    }
                    for item in state.items[0]
                ],
                "stock_quantities": [[item.stock_quantity for item in items_in_store] for items_in_store in state.items],
            },
        }
    )
