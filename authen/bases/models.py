from django.db import models
from django.utils import timezone, translation
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import (
    acheck_password,
    check_password,
    make_password,
)

from authen.bases.managers import TGUserManager


LANGUAGE_CHOICE = translation.trans_real.get_languages()

class TGOwnerAbstract(models.Model):
    # TGUSER_RELATE_FIELD = "" #check it
    
    class Meta:
        abstract=True
    
    def get_user(self):
        return getattr(self, self.TGUSER_RELATE_FIELD)
    
    def __str__(self):
        user = self.get_user()
        return getattr(user, user.USERNAME_FIELD)
    

class TGUserBaseAbstract(models.Model):
    # LANGUAGE_FIELD = "" #check it
    password = models.CharField("password", max_length=128)
    last_login = models.DateTimeField("last login", blank=True, null=True)

    is_active = True

    REQUIRED_FIELDS = []

    _password = None

    class Meta:
        abstract = True

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)
    
    def get_id(self):
        return getattr(self, self.USERNAME_FIELD)
    
    def get_language(self):
        return getattr(self, self.LANGUAGE_FIELD)
    
    def natural_key(self):
        return (self.get_username(), self.get_id())
    
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    async def acheck_password(self, raw_password):
        async def setter(raw_password):
            self.set_password(raw_password)
            self._password = None
            await self.asave(update_fields=["password"])

        return await acheck_password(raw_password, self.password, setter)
    
    def set_unusable_password(self):
        self.password = make_password(None)



class TGUserAbstract(TGUserBaseAbstract, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    user_id = models.BigIntegerField(
        "user id",
        primary_key=True
    )
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    language = models.CharField(
        "language", 
        choices=LANGUAGE_CHOICE, 
        max_length=25,
        default="en"
    )
    
    is_staff = models.BooleanField(
        "staff status",
        default=False,
    )

    is_active = models.BooleanField(
        "active",
        default=True,
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    objects = TGUserManager()

    ID_FIELD = "user_id"
    USERNAME_FIELD = "username"
    LANGUAGE_FIELD = "language"

    class Meta:
        abstract = True
        verbose_name = "user"
        verbose_name_plural = "users"