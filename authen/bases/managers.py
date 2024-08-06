from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from django.db import models

from typing import Any, Optional
from functools import partialmethod
from contextlib import suppress


class TGUserManager(UserManager):
    def _create_user(self, 
                     user_id, 
                     username: str,
                     password: Optional[str] = None, 
                     is_guard: bool = False,
                     is_staff: bool = False,
                     is_superuser: bool = False,
                     **extra_fields: Any):
        if not user_id:
            raise ValueError("The given user id must be set")
        
        if not username:
            raise ValueError("The given username must be set")

        password = make_password(password)

        user = self.model(password=password, 
                          user_id=user_id, 
                          username=username,
                          is_guard=is_guard,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          **extra_fields)
        user.save()
        return user
    
    create_user = partialmethod(_create_user,
                                is_staff=False,
                                is_superuser=False)
    
    create_superuser = partialmethod(_create_user,
                                     is_staff=True,
                                     is_superuser=True)

    def get_by_natural_key(self, user_id: str | None) -> Any:
        return self.get(**{self.model.ID_FIELD: user_id})
    

class TGOwnerManager(models.Manager):
    def create_owner(self, user_id, password, **extra_fields):
        owner_kwargs = {}
        for field in self.model._meta.get_fields():
            with suppress(KeyError):
                owner_kwargs.setdefault(field.name, extra_fields.pop(field.name))

        user = self.model._meta.get_field("tg_user").related_model._default_manager.create_user(
            user_id=user_id,
            password=password,
            **extra_fields
        )
        owner_kwargs["tg_user"] = user
        owner = self.model(**owner_kwargs)
        owner.save()
        return owner
    
    def get_by_natural_key(self, user_id):
        return self.model.get(tg_user__user_id=user_id)
    