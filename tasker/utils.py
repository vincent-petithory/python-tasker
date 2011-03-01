#-*- coding:utf-8 -*-

import subprocess
import shlex

def fail_on_error(raw_command, returncode):
    if returncode > 0:
        raise RuntimeError('command « %s » failed with exit code %d' % (raw_command, returncode))

def sh(*args):
    raw_command = ' '.join(arg for arg in args)
    command = shlex.split(raw_command)
    returncode = subprocess.call(command, shell=False)
    fail_on_error(raw_command, returncode)
    return returncode

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
    returncode = p.returncode
    fail_on_error(raw_command, returncode)
    return stdout, stderr, returncode

def shell(cmd):
    returncode = subprocess.call(cmd, shell=True)
    fail_on_error(cmd, returncode)
    return returncode

def shellp(cmd):
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = p.communicate()
    returncode = p.returncode
    fail_on_error(cmd, returncode)
    return stdout, stderr, returncode
