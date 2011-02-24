#-*- coding:utf-8 -*-

import subprocess
import shlex

def sh(*args):
    raw_command = ' '.join(arg for arg in args)
    command = shlex.split(raw_command)
    return subprocess.call(command, shell=False)

def shp(*args):
    raw_command = ' '.join(arg for arg in args)
    command = shlex.split(raw_command)
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    )
    stdout, stderr = p.communicate()
    return stdout, stderr, p.returncode

def shell(cmd):
    return subprocess.call(cmd, shell=True)

def shellp(cmd):
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = p.communicate()
    return stdout, stderr, p.returncode
