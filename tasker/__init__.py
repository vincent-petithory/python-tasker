#-*- coding:utf-8 -*-

version_info = (0,2,0)

import sys
import os
import imp

import tasker.utils

class Tasker(object):
    
    taskers = []
    
    @staticmethod
    def get_tasker_for_modulename(module_name):
        for tasker_obj in Tasker.taskers:
            if tasker_obj.task_modulename == module_name:
                return tasker_obj
        return None
    
    task_list = []
    taskfunc_list = []
    default_taskname = None
    task_module = None
    task_modulename = None
    task_basedir = None
    tasks = None
    
    EXTRA_IMPORTS = {
        'os': os,
        'sys': sys,
        'sh': tasker.utils.sh,
        'shp': tasker.utils.shp,
        'shell': tasker.utils.shell,
        'shellp': tasker.utils.shellp,
        'tar': tasker.utils.tar,
        'call_task': tasker.utils.call_task,
    }
    
    def __init__(self, task_file):
        Tasker.taskers.append(self)
        self.module_path = os.path.realpath(task_file)
        self.module_dirname = os.path.dirname(self.module_path)
        self.module_basename = os.path.basename(self.module_path)
        
        self.task_modulename, ext = os.path.splitext(self.module_path)
        del ext
        self.task_modulename = self.task_modulename.replace('/', '.')
        if self.task_modulename.startswith('.'):
            self.task_modulename = self.task_modulename[1:]
        
        self.task_basedir = self.module_dirname
        
        # cd in the task module directory by default
        os.chdir(self.module_dirname)
        
        # import the tasks module
        try:
            self.module_file = open(self.module_path, 'r')
            self.task_module = imp.load_module(self.task_modulename, self.module_file, self.module_path, ('.py', 'r', imp.PY_SOURCE))
            self.module_file.close()
            self.task_module.__dict__.update(Tasker.EXTRA_IMPORTS)
        except ImportError as ie:
            sys.stderr.write('Could not import the « %s » file in the directory « %s ».Reason: %s\n' % (self.task_modulename, self.module_dirname, ie))
            sys.exit(2)
        except Exception:
            sys.stderr.write('Exception caught in your « %s » init code.\n' % self.task_modulename)
            raise
    
    def init_context(self):
        # change to the correct directory
        os.chdir(self.task_basedir)
    
    def run(self, task_list):
        self.task_list = task_list
        # exit if not tasks defined
        if len(self.taskfunc_list) == 0: # filled with task() decorator
            sys.stdout.write('No tasks in « %s ». Exit.\n' % self.task_modulename)
            sys.exit(0)
        
        # get the default target
        if len(self.task_list) == 0:
            try:
                self.default_taskname = getattr(self.task_module, 'DEFAULT')
            except AttributeError:
                t1 = self.task_list[0]
                self.default_taskname = t1[len(t1)-1]
            else:
                try:
                    # check default task name exists, otherwise, exit
                    getattr(self.task_module, self.default_taskname)
                except AttributeError:
                    sys.stderr.write('Could not find the specified default task « %s ».\n' % self.default_taskname)
                    sys.exit(3)
                
        if len(self.task_list) == 0:
           self.task_list = [self.default_taskname]
        
        # evaluate the basedir of the task module
        try:
            relative_dir = getattr(self.task_module, 'BASEDIR')
        except AttributeError:
            relative_dir = '.'
        
        self.task_basedir = os.path.join(self.module_dirname, relative_dir)
        
        # init the context
        self.init_context()
        
        # execute the init function if defined
        try:
            INIT_FUNC = getattr(self.task_module, 'init')
        except AttributeError:
            # no init function was defined. Skip.
            pass
        else:
            INIT_FUNC()

        task_objects = []

        def get_task_with_name(name):
            for task_object in task_objects:
                if task_object.name == name:
                    return task_object
            return None

        for raw_task in self.taskfunc_list:
            n = len(raw_task)
            main_taskname = raw_task[n-1]
            dep_tasknames = []
            if n > 1:
                dep_tasknames = raw_task[:n-1]
            t = Task(name=main_taskname, tasker=self, namedepends=dep_tasknames)
            task_objects.append(t)

        for task_object in task_objects:
            task_object.resolve(task_objects, self.task_module)

        for task_name in self.task_list:
            task = get_task_with_name(task_name)
            try:
                task.process()
            except TaskError as te:
                sys.stderr.write('** tasker: Exception « %s » caught in task « %s »: %s\n' % (te.exception_type, te.name, te.message))
                sys.stderr.write('** tasker: Exiting.\n')
                sys.exit(1)

class TaskError(Exception):
    """An error while running a task."""
    def __init__(self, message, name, exception_type):
        self.message = message
        self.name = name
        self.exception_type = exception_type
    

class Task(object):
    """
        depends: list of other Task elements
    """
    name = None
    tasker = None
    
    def __init__(self, name, tasker, namedepends=None):
        self.name = name
        self.tasker = tasker
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
            self.tasker.init_context()
            self.func()
        except Exception as e:
            st = str(type(e))
            exception_type = st[st.find('\'')+1:st.rfind('\'')]
            raise TaskError(str(e), self.name, exception_type)
    
    def resolve(self, other_tasks, module):
        self.depends = []
        for namedepend in self.namedepends:
            for other_task in other_tasks:
                if namedepend == other_task.name:
                    if namedepend not in [d.name for d in self.depends]:
                        self.depends.append(other_task)
                    break;
        # notify which deps could not be resolved
        unresolved_deps = set(self.namedepends).difference(set([t.name for t in self.depends]))
        if len(unresolved_deps) > 0:
            raise AttributeError('Could not resolve task(s) « %s »' % ', '.join(unresolved_deps), self.name, 'TaskError')
        try:
            self.func = getattr(module, self.name)
        except AttributeError:
            sys.stderr.write('Could not find function « %s » in « %s ».\n' % (self.name, self.tasker.task_modulename))
            raise

# import the task decorator, as a shortcut when writing the tasks.py files
from tasker.decorators import task

