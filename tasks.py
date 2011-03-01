#-*- coding:utf-8 -*-
from tasker import task

DEFAULT = 'main'

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
    shell('rfgnoreng "ok"')

@task()
def clean():
    print('task:clean')

