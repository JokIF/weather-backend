from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model, authenticate
from django.middleware.csrf import rotate_token
from django.http import HttpRequest
from authen.models import TGUser

from authen.utils.classes import UserCredit


user_model: TGUser = get_user_model()
    

def user_get(request: HttpRequest):
    user_credit = UserCredit(request.headers)
    user = authenticate(request, 
                        user_id=user_credit.id
    )
    return user
    

class AuthenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = user_get(request)
        if request.user.is_authenticated:
            setattr(request, "_dont_enforce_csrf_checks", True) # разобраться с этим

        return self.get_response(request)
        