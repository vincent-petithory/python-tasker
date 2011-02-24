#-*- coding:utf-8 -*-

from tasker import task_list
from functools import wraps

class task(object):

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            f = args[0]
            if callable(f):
                # the decorator is called without args,
                # hence 1st arg is our function to decorate
                task_list.append((f.__name__, ))
                self._decorate(f)
            else:
                self.depends = args
        else:
            self.depends = ()

    def __call__(self, f):
        t = tuple(reversed(self.depends)) + (f.__name__, )
        task_list.append(t)
        return self._decorate(f)
    
    def _decorate(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper

