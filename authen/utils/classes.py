from functools import partial


#user-<user_name>
#token-<token_name>
#password-<password_name>

class UserCredit:
    def __init__(self, mapped, prefix="user", sep="-"):
        self.mapped = mapped
        self._prefix = prefix
        self._sep = sep

    def _get_name(self, name: str):
        return self.mapped.get(f"{self._prefix}{self._sep}{name}")
    
    token = property(partial(_get_name, name="token"))
    id = property(partial(_get_name, name="id"))
    password = property(partial(_get_name, name="password"))