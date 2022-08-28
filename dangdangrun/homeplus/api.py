from typing import Optional

import aiohttp

from .models import Item


class HomeplusAPIException(Exception):
    pass


class HomeplusAPI:

    session: aiohttp.ClientSession

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_item(self, item_no: str, store_id: Optional[int] = None) -> Item:
        async with self.session.get(
            f'https://front.homeplus.co.kr/item/getItemDetail.json?itemNo={item_no}&storeType=HYPER{"" if store_id is None else f"&storeId={store_id}"}'
        ) as response:
            data = await response.json()
            if data["data"] is None:
                print(f"store_id={store_id} 에서 item_no={item_no} 를 가져오는데 실패했습니다.")
                raise HomeplusAPIException(data["returnMessage"])

            item = Item(
                no=data["data"]["item"]["basic"]["itemNo"],
                name=data["data"]["item"]["basic"]["itemNm"],
                store_id=int(data["data"]["item"]["basic"]["storeId"]),
                stock_quantity=int(data["data"]["item"]["sale"]["stockQty"]),
            )
            return item
