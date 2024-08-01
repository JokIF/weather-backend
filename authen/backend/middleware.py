from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model, authenticate
from django.http import HttpRequest
from authen.models import TGUser
from django.http.request import HttpHeaders

from functools import partial


user_model: TGUser = get_user_model()


#user-<user_name>
#token-<token_name>
#password-<password_name>

class UserCredit:
    def __init__(self, mapped_, prefix="user", sep="-"):
        self.mapped_ = mapped_
        self._prefix = prefix
        self._sep = sep

    def _get_name(self, name: str):
        return self.mapped_.get(f"{self._prefix}{self._sep}{name}")
    
    token = property(partial(_get_name, name="token"))
    id = property(partial(_get_name, name="id"))
    password = property(partial(_get_name, name="password"))

    

def user_get(request: HttpRequest):
    user_credit = UserCredit(request.headers)
    if token := user_credit.token:
        user = authenticate(request, sesame=token) # needed complete
    else:
        user = authenticate(request, 
                            user_id=user_credit.id,
                            password=user_credit.password
        )
    return user
    

class AuthenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = user_get(request)
        return self.get_response(request)
        