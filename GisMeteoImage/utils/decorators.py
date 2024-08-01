from functools import reduce
from typing import Any


def JsonData(mapping):
    def json_data(*names):
        def wrapper_outer(func):
            def wrapper_inner(self, *args, **kwargs):
                return func(self, 
                            reduce(lambda dict_, name: dict_[name], (getattr(self, mapping), *names)),
                            *args, 
                            **kwargs)
            return wrapper_inner
        return wrapper_outer
    return json_data
        
