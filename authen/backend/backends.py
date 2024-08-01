from django.contrib.auth.backends import ModelBackend as ModelBackendStd
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


UserModel = get_user_model()


class ModelBackend(ModelBackendStd):
    def authenticate(self, request, user_id=None, password=None, **kwargs):
        if user_id is None:
            user_id = kwargs.get(UserModel.ID_FIELD)
        if user_id is None or password is None:
            return AnonymousUser()
        try:
            user = UserModel._default_manager.get_by_natural_key(user_id)
        except UserModel.DoesNotExist:
            return AnonymousUser()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            return AnonymousUser()
            
