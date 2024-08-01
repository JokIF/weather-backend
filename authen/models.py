from django.db import models

from authen.bases.models import TGUserAbstract, TGOwnerAbstract
from authen.bases.managers import TGOwnerManager
from authen.bases.mixins import TicketsMixin

class TGUser(TGUserAbstract, TicketsMixin):
    class Meta:
        db_table = "TGUser"


class TGOwner(TGOwnerAbstract):
    first_name = models.CharField("first name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=True)

    tg_user = models.OneToOneField(
        to=TGUser,
        on_delete=models.CASCADE,
        related_name="owner",
        verbose_name="TgUserRelate",
        to_field="user_id",
        primary_key=True
    )
    lat = models.DecimalField(
        verbose_name="latitude",
        decimal_places=6,
        max_digits=9,
        blank=True,
        null=True, # more options
    )
    lon = models.DecimalField(
        verbose_name="longitude", 
        decimal_places=6,
        max_digits=9,
        blank=True,
        null=True, # more oprions
    ) 
    city = models.CharField(
        verbose_name="city",
        blank=True,
        null=True,
        max_length=84
        )

    TGUSER_RELATE_FIELD = "tg_user"

    objects = TGOwnerManager()

    class Meta:
        db_table = "TGOwner"
        verbose_name = "owner"

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        return self.first_name    
