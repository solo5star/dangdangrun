import asyncio
from typing import List

import discord
from dangdangrun import settings
from dangdangrun.client import Client
from dangdangrun.state import state
from discord.ext import commands

from .embeds import create_stock_brief_embed, create_stock_change_embed

client = Client(settings.SERVER_HOST)
bot = commands.Bot(command_prefix="!")


def get_guilds() -> List[discord.Guild]:
    guilds: List[discord.Guild] = [bot.get_guild(settings.DISCORD_DEBUG_SERVER_ID)] if settings.DEBUG else bot.guilds
    guilds = filter(bool, guilds)
    return guilds


class Topic:
    topic: str

    def __init__(self, topic: str) -> None:
        self.topic = topic

    async def create_category(self) -> None:
        guilds = get_guilds()
        tasks = []
        for guild in guilds:
            category = next((category for category in guild.categories if category.name == self.topic), None)
            if category is None:
                tasks.append(guild.create_category(self.topic))

        await asyncio.gather(*tasks)

    async def create_text_channel(self, channel_name: str) -> None:
        guilds = get_guilds()
        tasks = []
        for guild in guilds:
            # check category exists
            category = next((category for category in guild.categories if category.name == self.topic), None)
            if category is None:
                print(f"Warning: create text channel in server (server_id={guild.id}) failed. reason: category {self.topic} not exists.")
                continue

            # check channel exists and create
            if not next((channel for channel in guild.channels if channel.name == channel_name), None):
                tasks.append(guild.create_text_channel(channel_name, category=category))

        await asyncio.gather(*tasks)

    def get_channels(self, channel_name: str) -> List[discord.TextChannel]:
        guilds = get_guilds()
        channels = []
        for guild in guilds:
            for channel in guild.text_channels:
                if channel.category is not None and channel.category.name == self.topic and channel.name == channel_name:
                    channels.append(channel)

        return channels

    async def send(self, channel_name: str, *args, **kwargs):
        tasks = []
        for channel in self.get_channels(channel_name):
            tasks.append(channel.send(*args, **kwargs))

        await asyncio.gather(*tasks)

    async def edit_last_message(self, channel_name: str, *args, **kwargs):
        tasks = []
        for channel in self.get_channels(channel_name):

            async def task():
                message: discord.Message = await channel.fetch_message(channel.last_message_id)
                if message is not None and message.author == bot.user:
                    await message.edit(*args, **kwargs)
                else:
                    await channel.send(*args, **kwargs)

            tasks.append(task())

        await asyncio.gather(*tasks)


@bot.event
async def on_ready():
    print("Bot ready!")
    announce_channel = Topic("당당치킨봇")
    await announce_channel.create_category()
    await announce_channel.create_text_channel("시스템")


@client.on_update_stores
async def on_update_stores():
    print("stores updated")
    for region in state.regions:
        region_channel = Topic(f"당당치킨 {region}")
        await region_channel.create_category()
        await region_channel.create_text_channel("재고현황")
        await region_channel.create_text_channel("입고현황")


@client.on_update_items
async def on_update_items():
    print("items updated")
    for region in state.regions:
        region_channel = Topic(f"당당치킨 {region}")

        embed = create_stock_brief_embed(region)
        if embed is not None:
            await region_channel.edit_last_message("재고현황", embed=embed)

        embed = create_stock_change_embed(region)
        if embed is not None:
            await region_channel.send("입고현황", embed=embed)


@client.on_close
async def on_close():
    announce_channel = Topic("당당치킨봇")
    await announce_channel.send("알림", "dangdangrun 서버와 연결이 끊겼습니다. 오프라인이거나 다운되었을 수 있습니다. 서버 연결이 끊긴 동안에는 업데이트가 되지 않습니다.")


@client.on_open
async def on_open():
    announce_channel = Topic("당당치킨봇")
    await announce_channel.send("알림", "dangdangrun 서버에 연결하였습니다.")


loop = asyncio.get_event_loop()
try:
    loop.create_task(bot.start(settings.DISCORD_TOKEN))
    loop.create_task(client.run())
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(bot.close())
finally:
    loop.close()
