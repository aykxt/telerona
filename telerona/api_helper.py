import asyncio
import logging

import aiohttp

from . import bot

logger = logging.getLogger(__name__)


class Api:
    api_link = "https://corona.lmao.ninja/v2"
    interval = 1800

    def __init__(self):
        self.countries = None
        self.glob = None
        bot.loop.create_task(self.check_updates())

    async def check_updates(self):
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(self.api_link + "/all") as response:
                    self.glob = await response.json()

                async with session.get(
                    self.api_link + "/countries?sort=cases"
                ) as response:
                    self.countries = await response.json()

                logger.info("New data fetched.")
                await asyncio.sleep(self.interval)
