#-*- coding:utf-8 -*-
from tasker import task

from tasker.utils.shell import *
from tasker.utils import call_task, tar

# defaults to the first task defined, if omitted
DEFAULT = 'main'

# defaults to . if omitted
BASEDIR = '.'

# is executed at startup. optional
def init():
    print('initializing...')

@task('hello', 'clean')
def main():
    print('task:main')
    raise AttributeError('error i want')

@task()
def hello():
    print('task:hello')
    o,e,c = shp('echo "ok"')
    print(o, e, c)
    sh('echo "ok"')
    
    o,e,c = shellp('echo "ok"')
    print(o, e, c)

@task()
def clean():
    print('task:clean')

@task()
def subtask():
    call_task(__file__, 'clean')

@task()
def tar_test():
    tar('data', 'data.tar.gz')
