#-*- coding:utf-8 -*-

from tasker import Tasker
from functools import wraps
import collections

class task(object):
    
    related_tasker = None
    
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            f = args[0]
            if isinstance(f, collections.Callable):
                # the decorator is called without args,
                # hence 1st arg is our function to decorate
                self.related_tasker = Tasker.get_tasker_for_modulename(f.__module__)
                self.related_tasker.taskfunc_list.append((f.__name__, ))
                self._decorate(f)
            else:
                self.depends = args
        else:
            self.depends = ()

    def __call__(self, f):
        t = tuple(self.depends) + (f.__name__, )
        self.related_tasker = Tasker.get_tasker_for_modulename(f.__module__)
        self.related_tasker.taskfunc_list.append(t)
        return self._decorate(f)
    
    def _decorate(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper

