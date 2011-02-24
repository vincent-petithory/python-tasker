#!/usr/bin/env python
#-*- coding:utf-8 -*-

from distutils.core import setup
from tasker import version_info

version = '.'.join(str(v) for v in version_info)

data = dict(
    name =          'tasker',
    version =       version,
    url =           'http://blog.lunar-dev.net',
    download_url =  '',
    description =   'Python utility similar to make.',
    author =        'Vincent Petithory',
    author_email =  'vincent [dot] petithory [at] gmail.com',
    maintainer =    'Vincent Petithory',
    maintainer_email = 'vincent [dot] petithory [at] gmail.com',
    license =       'GPL License',
    packages =      ['tasker'],
    scripts =       ['bin/tasker'],
    cmdclass =      {},
    classifiers =   ['Development Status :: 5 - Production/Stable',
                     'License :: OSI Approved :: GPL License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2',
                     'Programming Language :: Python :: 2.3',
                     'Programming Language :: Python :: 2.4',
                     'Programming Language :: Python :: 2.5',
                     'Programming Language :: Python :: 2.6',
                    ],
    ) 

setup(**data)
