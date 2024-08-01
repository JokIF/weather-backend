from django.utils.translation import get_language

from abc import ABC
from dataclasses import dataclass
from typing import Any, Optional


#Base for parser
class BaseDataParser:
    def __init__(self, data: dict, lang: Optional[str]) -> None:
        self.data = data
        self.lang = lang or get_language()

#As Response after request to gismeteoAPI
@dataclass
class GismeteoResponse:
    raw: dict
    parsed: BaseDataParser

# Manual for parser
@dataclass
class ManualData:
    action_name: str
    content_name: str
    coords: tuple[int, int]
    kwargs: dict[str, Any]

Manual = tuple[tuple[ManualData]]

#Dataclass for image field
@dataclass
class ImageGetter:
    url: str
    path: str
