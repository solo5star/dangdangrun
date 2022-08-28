import os

from dotenv import load_dotenv

from .homeplus.constants import regions

load_dotenv()

REGIONS = list(filter(lambda region: region in regions, map(lambda region: region.strip(), os.getenv("REGIONS", "부산").split(","))))

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_DEBUG_SERVER_ID = int(os.getenv("DISCORD_DEBUG_SERVER_ID", 0))

SERVER_HOST = os.getenv("SERVER_HOST", "ws://localhost:3355")

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
