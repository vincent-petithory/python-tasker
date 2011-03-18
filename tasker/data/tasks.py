#-*- coding:utf-8 -*-
from tasker import task

# defaults to the first task defined, if omitted
DEFAULT = 'main'

# defaults to . if omitted
BASEDIR = '.'

# is executed at startup. optional
def init():
    pass

@task()
def main():
    pass
