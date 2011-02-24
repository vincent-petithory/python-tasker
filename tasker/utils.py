#-*- coding:utf-8 -*-

import subprocess
import shlex

def _getcmd(*args):
    raw_command = ' '.join(arg for arg in args)
    command = shlex.split(raw_command)
    return command

def _sh_with_pipe(*args, **kwargs):
    shell = kwargs.get('shell')
    p = subprocess.Popen(_getcmd(*args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    stdout, stderr = p.communicate()
    return stdout, stderr, p.returncode

def sh(*args):
    return _sh_with_pipe(*args, shell=False)

def shell(*args):
    return _sh_with_pipe(*args, shell=True)
