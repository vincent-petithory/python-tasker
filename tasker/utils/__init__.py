#-*- coding:utf-8 -*-

def call_task(task_file, *tasks):
    from tasker import Tasker
    subtasker = Tasker(task_file)
    subtasker.run(tasks)

def tar(directory, tarfilepath):
    """
        Creates a tar file from a directory.
        Will apply gz or bz2 compression using the given tar filename
    """
    import tarfile
    import os
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

