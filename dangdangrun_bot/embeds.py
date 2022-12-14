import itertools
from typing import List, Optional

import discord
from dangdangrun.homeplus.models import Store
from dangdangrun.state import state

MESSAGE_UPDATED_TIME = "κΈ°μ€: {last_updated:%Y-%m-%d %H:%M:%S}"
MESSAGE_ITEM_LINKS_TITLE = "π κ΅¬λ§€ λ§ν¬"
MESSAGE_ITEM_LINKS_LINK = (
    '[{item.name}](https://front.homeplus.co.kr/item?itemNo={item.no}&storeType=HYPER "ννλ¬μ€ {item.name} κ΅¬λ§€ νμ΄μ§λ‘ μ΄λνλ €λ©΄ ν΄λ¦­νμΈμ")'
)

MESSAGE_STOCK_BREIF_TITLE = "[{region}] μ¬κ³  νν©"
MESSAGE_STOCK_BREIF_STORE = "{store.name}"
MESSAGE_STOCK_BREIF_ITEM = "{icon} {item.name}: **{item.stock_quantity}**"
MESSAGE_STOCK_BREIF_CHANGES_TITLE = "π μ¬κ³  λ³λ μ΄λ ₯"
MESSAGE_STOCK_BREIF_CHANGES_CHANGE = "[{stock_change.time:%m/%d %H:%M:%S}][{stock_change.store.name}] {icon} {stock_change.item.name}: ~~{stock_change.previous}~~β**{stock_change.current}**"
MESSAGE_STOCK_BREIF_CHANGES_EMPTY = "*λ³λ μ΄λ ₯μ΄ μμ΅λλ€*"

MESSAGE_STOCK_CHANGE_TITLE = "[{region}] {store_names} μ¬κ³  λ³λ"
MESSAGE_STOCK_CHANGE_CHANGED = "{icon} {item.name}: ~~{previous}~~β**{current}**"
MESSAGE_STOCK_CHANGE_NOT_CHANGED = "{icon} {item.name}: {current}"


def create_base_embed(title: str, description: Optional[str] = None) -> discord.Embed:
    last_updated = state.last_updated

    embed = discord.Embed(
        title=f"π {title}",
        description="\n".join([description or "", MESSAGE_UPDATED_TIME.format(last_updated=last_updated)]),
    )
    return embed


def add_footer(embed: discord.Embed):
    items = state.items
    embed.add_field(
        name=MESSAGE_ITEM_LINKS_TITLE,
        inline=False,
        value=" | ".join([MESSAGE_ITEM_LINKS_LINK.format(item=item) for item in items[0]]),
    )


def create_stock_brief_embed(region: str) -> Optional[discord.Embed]:
    stores, items, stock_changes = state.stores, state.items, state.stock_changes

    if items is None:
        return None

    embed = create_base_embed(MESSAGE_STOCK_BREIF_TITLE.format(region=region))
    for i, items_in_store in enumerate(items):
        store = stores[i]
        if store.region != region:
            continue

        stock_messages = []

        for j, item in enumerate(items_in_store):
            # display current stock state
            icon = "β" if item.stock_quantity > 0 else "β"
            stock_messages.append(MESSAGE_STOCK_BREIF_ITEM.format(icon=icon, item=item))

        embed.add_field(
            name=MESSAGE_STOCK_BREIF_STORE.format(store=store),
            value="\n".join(stock_messages),
        )

    # display stock changes
    embed.add_field(
        name=MESSAGE_STOCK_BREIF_CHANGES_TITLE,
        inline=False,
        value="\n".join(
            map(
                lambda stock_change: MESSAGE_STOCK_BREIF_CHANGES_CHANGE.format(
                    stock_change=stock_change,
                    icon="β" if stock_change.current > 0 else "β",
                ),
                # take 8 of given region from stock_changes
                reversed(
                    list(itertools.islice(filter(lambda stock_change: stock_change.store.region == region, reversed(stock_changes)), 8))
                ),
            )
        )
        or MESSAGE_STOCK_BREIF_CHANGES_EMPTY,
    )

    add_footer(embed)
    return embed


def create_stock_change_embed(region: str) -> Optional[discord.Embed]:
    stores, previous_items, items = state.stores, state.previous_items, state.items

    if previous_items is None or items is None:
        return None

    embed = create_base_embed(title="-")
    updated_stores: List[Store] = []

    def stock_change_function(previous: int, current: int) -> bool:
        return (previous == 0) != (current == 0)

    for i, items_in_store in enumerate(items):
        store = stores[i]
        if store.region != region:
            continue

        # detect stock quantity difference
        has_any_updates = any(
            map(
                lambda j: stock_change_function(previous_items[i][j].stock_quantity, items[i][j].stock_quantity), range(len(items_in_store))
            )
        )

        if not has_any_updates:
            continue

        updated_stores.append(store)
        stock_messages = []

        for j, item in enumerate(items_in_store):
            previous_item = previous_items[i][j]
            stock_changed = previous_item.stock_quantity != item.stock_quantity

            icon = "β" if item.stock_quantity > 0 else "β"
            previous = "νλ§€μ€" if previous_item.stock_quantity > 0 else "νμ "
            current = "νλ§€μ€" if item.stock_quantity > 0 else "νμ "

            if stock_changed:
                stock_messages.append(
                    MESSAGE_STOCK_CHANGE_CHANGED.format(
                        icon=icon,
                        item=item,
                        previous=previous,
                        current=current,
                    )
                )
            else:
                stock_messages.append(
                    MESSAGE_STOCK_CHANGE_NOT_CHANGED.format(
                        icon=icon,
                        item=item,
                        current=current,
                    )
                )

        embed.add_field(name=f"{store.name} ({store.region})", value="\n".join(stock_messages))

    embed.title = MESSAGE_STOCK_CHANGE_TITLE.format(
        region=region,
        store_names=", ".join(map(lambda store: store.name, updated_stores)),
    )
    add_footer(embed)

    return embed if len(updated_stores) > 0 else None
