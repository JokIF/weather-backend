from django.db import models
from django.db.models.fields.json import KT
from django.utils.translation import get_language
from django.conf import settings
from django.core.files import File
from django.utils.timezone import now
from PIL.Image import Image, open as open_image, alpha_composite

from GisMeteoImage.core import GismeteoParser, GismeteoResponse
from GisMeteoImage.core.draw import GismeteoDrawer
from GisMeteoImage.core.classes import ImageGetter
from GisMeteoImage.utils.gismeteo_data import gismeteo_response_from_raw_data

from datetime import timedelta
from uuid import uuid4
from typing import List, Optional, Union
import os
from pathlib import Path


class ResponseGismeteoManager(models.Manager):
    @staticmethod
    async def make_request(lat, lon):
        raw_data: Optional[GismeteoResponse] = await settings.GISMETEO_API._request(
            url=settings.GISMETEO_API.FORECAST_URL.format(
                lat=lat, 
                lon=lon, 
                lang=get_language()
            )
        )

        return raw_data
    
    async def acreate(self, raw_data, user):
        if raw_data is None or raw_data.get("errors"):
            raw_data = await self.make_request(lat=user.owner.lat, lon=user.owner.lon)
        return await super().acreate(raw_data=raw_data, user=user, city=user.owner.city)
    
    def find_around_time(self, city: str, now_time, delta_time=90): #поменять название
        delta_time = timedelta(minutes=delta_time)
        return self.filter(
            city=city, 
            time_at__gte=now_time-delta_time, 
            time_at__lte=now_time+delta_time
            ).first()
        


class ResponseGismeteoModel(models.Model):
    image_field = models.ImageField("image",
                                    null=True,
                                    default=None,
                                    upload_to="gismeteo_images") #подробнее параметры # upload_to
    raw_data = models.JSONField("raw_data",
                                null=True,
                                blank=True)
    user = models.ForeignKey(to="authen.TGUser",
                             to_field="user_id",
                             on_delete=models.SET_NULL,
                             related_name="gis_response",
                             verbose_name="requested_user",
                             null=True)
    city = models.CharField("city",
                            max_length=84)
    time_at = models.DateTimeField(auto_now=True)

    objects = ResponseGismeteoManager()

    class Meta:
        db_table="ResponseGismeteo"

    def save(self, *args, **kwargs) -> None:
        if self.image is None:
            self.make_image()
        return super().save(*args, **kwargs)
    
    async def asave(self, *args, **kwargs) -> None:
        if self.image is None:
            self.make_image()
        return await super().asave(*args, **kwargs)
    
    def make_image(self) -> str: # task for celery
        try:
            gis_resp = gismeteo_response_from_raw_data(self.raw_data, many=True)
        except KeyError:
            return None
        
        filtred_resp = settings.GISMETEO_API.filter_days(gis_resp, now())
        setattr(filtred_resp[0], "city", self.city)
        drawer = GismeteoDrawer(filtred_resp)

        with open_image(settings.GISMETEO_IMAGE_TEMPLATE_PNG) as template:
            with drawer.blank_frame_from_template(temlate_image=template) as blank_frame:
                drawer.manually_draw(blank_frame, template.mode)
                out_image = alpha_composite(template, blank_frame)
        
        image_name = self.create_image_name()
        out_image.save(image_name)

        self.image = image_name
        return self.image

    @property
    def image(self) -> Optional[str]:
        try:
            return ImageGetter(
                path=self.image_field.path,
                url=self.image_field.url
                )
        except ValueError:
            return None
    
    @image.setter
    def image(self, pathOrStr: Union[os.PathLike, str]) -> None:
        image_name = os.path.basename(pathOrStr)
        
        with open(pathOrStr, "rb") as image_opend: #async open
            self.image_field.save(
                name=image_name,
                content=File(image_opend),
                save=False
            )
    
    @classmethod
    def create_image_name(cls):
        return Path(settings.MEDIA_ROOT) \
            / cls.image_field.field.upload_to \
                / f"{str(uuid4())}.png" #MEDIA_ROOT_CHANGE
    

ResponseGismeteoModel.objects.all()