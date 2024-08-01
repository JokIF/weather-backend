from aiohttp import ClientSession
from django.utils.timezone import now
from django.conf import settings
import ujson

from GisMeteoImage.core.gismeteoParser import GismeteoParser
from GisMeteoImage.core.classes import GismeteoResponse
from GisMeteoImage.utils.gismeteo_data import get_test_data, gismeteo_response_from_raw_data

import asyncio
from typing import List, Optional
from datetime import datetime
from itertools import dropwhile


class GismeteoAPI:
    BASE_URL = "https://api.gismeteo.net/v2/weather/"
    BASE_URL_PARAMS = "?latitude={lat}&longitude={lon}&lang={lang}"
    TODAY_URL = BASE_URL + "current/" + BASE_URL_PARAMS
    FORECAST_URL = BASE_URL + "forecast/" + BASE_URL_PARAMS + "&days=2"

    def __init__(self, TOKEN) -> None:
        self._header_token = {"X-Gismeteo-Token": TOKEN} #поменять на самостоятельное взятие

    async def _request(self, url, many=True):
        if settings.DEBUG is True:
            raw_data = get_test_data()
            return raw_data
        
        async with ClientSession() as session:
            async with session.get(url=url, headers=self._header_token) as response:
                if response.status == 200:
                    raw_data = await response.json()
                    return raw_data
                err = await response.json()
                #logger


    async def get_couple_days(self, lat, lon, lang):
        days: Optional[GismeteoResponse] = await self._request(
            url=self.FORECAST_URL.format(
                lat=lat, 
                lon=lon, 
                lang=lang
            )
        )
        if days is None:
            return
        filtred = self.filter_days(days, now=now())
        return filtred

    def filter_days(self, days: GismeteoResponse, now: datetime): #разделить
        now_user_time: datetime = now + days.parsed[0].tz.utcoffset(now)
        now_user_time = now_user_time.replace(tzinfo=days.parsed[0].tz)
        partial_data = list(dropwhile(lambda r: (now_user_time - r.local).seconds > 10800, days.parsed))[:4]
        return partial_data


# asyncio.run(GismeteoAPI("64144378d865c3.44623570").get_couple_days(
#     lat=55.75,
#     lon=37.6167,
#     lang="en"
# ))

# asyncio.run(GismeteoAPI("64144378d865c3.44623570").filter_days(gismeteo_response_from_raw_data(get_test_data()), datetime.utcnow()))

