#-*- coding:utf-8 -*-

version_info = (0,1,0)


import sys
import os

task_list = []
DEFAULT_TASKNAME = None
TASK_MODULE = None
TASK_MODULENAME = None
TASKS = None

class TaskError(Exception):
    """An error while running a task."""
    def __init__(self, message, name):
        self.message = message
        self.name = name
    

class Task(object):
    """
        depends: list of other Task elements
    """
    
    def __init__(self, name, namedepends=None):
        self.name = name
        self.func = None
        if namedepends is None:
            self.namedepends = ()
        else:
            self.namedepends = namedepends
    
    def process(self):
        if self.depends:
            for dep in self.depends:
                dep.process()
        try:
            #print 'exec', type(self.func)
            self.func()
        except Exception as e:
            #message = 'Exception caught in task « %s »: %s\n' % (self.name, e)
            raise TaskError(str(e), self.name)
            sys.exit(os.EX_SOFTWARE)
    
    def resolve(self, other_tasks, module):
        self.depends = []
        #print self.namedepends
        for namedepend in self.namedepends:
            for other_task in other_tasks:
                if namedepend == other_task.name:
                    if namedepend not in [d.name for d in self.depends]:
                        self.depends.append(other_task)
                    break;
        # notify which deps could not be resolved
        unresolved_deps = set(self.namedepends).difference(set([t.name for t in self.depends]))
        if len(unresolved_deps) > 0:
            sys.stderr.write('Could not resolve task(s) « %s ». Exit.\n' % ', '.join(unresolved_deps))
            sys.exit(os.EX_SOFTWARE)
        try:
            self.func = getattr(module, self.name)
        except AttributeError:
            sys.stderr.write('Could not find function « %s » in « %s ».\n' % (self.name, DEFAULT_TASKNAME))
            raise
