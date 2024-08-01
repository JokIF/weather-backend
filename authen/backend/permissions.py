from rest_framework.permissions import BasePermission, IsAdminUser
from django.contrib.auth import get_user_model


class BaseIsAdminOrOwner(BasePermission):
    user_from_obj = None

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_staff):
            return True
        
        user = getattr(obj, self.user_from_obj) if self.user_from_obj else obj
        return bool(user == request.user)
    

class TGIsAdminOrOwner(BaseIsAdminOrOwner):
    user_from_obj = "tg_user" #поменять после TGOwnerModel
