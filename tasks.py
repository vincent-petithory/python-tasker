#-*- coding:utf-8 -*-

import os
from tasker.decorators import task
from tasker.utils import sh, shell

DEFAULT = 'main'

@task('hello', 'clean')
def main():
    print('task:main')
    raise AttributeError('error i want')

@task()
def hello():
    print('task:hello')
    o,e,c = sh('echo "ok"')
    print(o, e, c)

@task()
def clean():
    print('task:clean')

