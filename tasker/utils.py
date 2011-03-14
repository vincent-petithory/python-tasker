#-*- coding:utf-8 -*-

import subprocess
import shlex
import os

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

def tar(directory, tarfilepath):
    """
        Creates a tar file from a directory.
        Will apply gz or bz2 compression using the given tar filename
    """
    import tarfile
    path, ext = os.path.splitext(tarfilepath)
    del path
    if ext == '.gz':
        mode = 'w:gz'
    elif ext == '.bz2':
        mode == 'w:bz2'
    else:
        mode = 'w'
    tar_file = tarfile.open(tarfilepath, mode)
    for prefix, dirs, files in os.walk(directory):
        for d in dirs:
            tar_file.add(os.path.join(prefix, d))
        if prefix == directory:
            for f in files:
                tar_file.add(os.path.join(prefix, f))
    tar_file.close()

def call_task(task_file, *tasks):
    from tasker import Tasker
    subtasker = Tasker(task_file)
    subtasker.run(tasks)
