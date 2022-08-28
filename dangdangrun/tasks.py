import asyncio
from datetime import datetime
from typing import Dict, List

import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .homeplus.api import HomeplusAPI
from .homeplus.models import Item
from .server import broadcast_items
from .state import State, state

item_no_list = [
    "069150196",  # 당당 후라이드 치킨
    "069150200",  # 당당 양념 치킨
    # "069034845",  # 버터링 딥초코 (테스트용)
]


def get_cron_schedule() -> Dict:
    now = datetime.now().strftime("%H:%M:%S")
    if "07:40:00" <= now <= "09:20:00":
        return {"second": "2,22,42"}

    if "06:30:00" <= now <= "20:00:00":
        return {"second": "2"}

    return {"minute": "0,10,20,30,40,50"}


def preprocess_items(items: List[List[Item]]) -> List[List[Item]]:
    for items_in_store in items:
        for item in items_in_store:
            if item.no in ["069150196", "069150200"]:
                item.name = item.name.rstrip("치킨").strip()

    return items


scheduler = AsyncIOScheduler(
    # suppress PytzUsageWarning: The zone attribute is specific to pytz's interface; please migrate to a new time zone provider
    timezone="Asia/Seoul"
)


@scheduler.scheduled_job("cron", id="crawling", second="2", next_run_time=datetime.now())
async def crawling_job():
    async with aiohttp.ClientSession() as session:
        api = HomeplusAPI(session)

        items: List[List[Item]] = await asyncio.gather(
            *[asyncio.gather(*[api.get_item(item_no, store.id) for item_no in item_no_list]) for store in state.stores]
        )

    state.update(
        State(
            items=preprocess_items(items),
        )
    )
    await broadcast_items()

    scheduler.reschedule_job("crawling", trigger="cron", **get_cron_schedule())
