#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from distutils.core import setup
from tasker import version_info

version = '.'.join(str(v) for v in version_info)

data = dict(
    name =          'tasker',
    version =       version,
    url =           'https://github.com/vincent-petithory/python-tasker',
    download_url =  '',
    description =   'Python utility similar to make.',
    author =        'Vincent Petithory',
    author_email =  'vincent [dot] petithory [at] gmail.com',
    maintainer =    'Vincent Petithory',
    maintainer_email = 'vincent [dot] petithory [at] gmail.com',
    license =       'GPL License',
    packages =      ['tasker', 'tasker.utils',],
    package_data =  {'tasker': ['data/tasks.py']},
    scripts =       ['bin/tasker'],
    cmdclass =      {},
    classifiers =   ['Development Status :: 5 - Production/Stable',
                     'License :: OSI Approved :: GPL License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3',
                    ],
    ) 

setup(**data)
