from PIL.Image import Image, new as ImageNew
from PIL.ImageFont import FreeTypeFont, truetype
from PIL.ImageDraw import ImageDraw
from django.conf import settings

from GisMeteoImage.core.classes import GismeteoResponse, Manual
from GisMeteoImage.core.draw.mixins import BaseDrawMixin

from abc import ABC
from typing import Optional, Union
from collections.abc import Iterable
from contextlib import contextmanager


class AbstractDrawer(ABC):
    STD_MODE = "RGBA"

    def __init__(self, 
                 font: Union[str, FreeTypeFont]=None, 
                 font_size: int=None
                 ) -> None:
        self._font = font or settings.GISMETEO_IMAGE_DEFAULT_FONT_TYPE
        self._font_size = font_size or settings.GISMETEO_IMAGE_DEFAULT_FONT_SIZE
    
    def draw(self, 
             draw_name: str,
             content: str,
             frame: Image,
             coords: tuple[int, int],
             mode: Optional[str] = None,
             font: Union[str, FreeTypeFont, None] = None,
             font_size: int = None,
             **kwargs
             ) -> None:
        font = self.normalize_font(font or self._font, 
                                   font_size or self._font_size)
        mode = mode or self.STD_MODE
        frame = ImageDraw(frame, mode=mode)
        getattr(self, draw_name)(content=content, frame=frame, coords=coords, font=font, **kwargs)

    @staticmethod
    def normalize_font(font: Union[str, FreeTypeFont], font_size: Optional[int] = None):
        if isinstance(font, FreeTypeFont):
            return font
        if isinstance(font, str):
            return truetype(font, font_size)
        raise TypeError("font must be string or FreeTypeFont")



class BaseManuallyDrawer(AbstractDrawer, ABC):
    MANUAL: Manual
    def __init__(self, 
                 manual_data: Union[GismeteoResponse, tuple[GismeteoResponse]], 
                 font=None, 
                 font_size=None) -> None:
        if not isinstance(manual_data, Iterable):
            manual_data = (manual_data,)

        if len(manual_data) != len(self.MANUAL):
            raise TypeError(f"manual_data must containts {len(self.MANUAL)} elements, but have {len(manual_data)}")
        
        self._manual_data = zip(self.MANUAL, manual_data)
        super().__init__(font, font_size)

    def manually_draw(self, frame: Image, mode: str = None):
        for rules, content_object in self._manual_data:
            for rule in rules:
                self.draw(
                    draw_name=rule.action_name,
                    content=getattr(content_object, rule.content_name),
                    frame=frame,
                    coords=rule.coords,
                    mode=mode,
                    **rule.kwargs
                )


class BaseDrawer(BaseManuallyDrawer, BaseDrawMixin):
    @classmethod
    def create_new_blank_frame(cls, size: tuple[int, int], mode: Optional[str] = None):
        if mode is None:
            mode = cls.STD_MODE
        return ImageNew(mode=mode, size=size)
    
    @classmethod
    @contextmanager
    def blank_frame_from_template(cls, temlate_image: Image):
        blank = cls.create_new_blank_frame(size=temlate_image.size, mode=temlate_image.mode)
        yield blank
        blank.close()
    

