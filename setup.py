#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from distutils.core import setup

__version_info__ = (0, 0, 1)
__version__ = '.'.join([str(v) for v in __version_info__])

setup(
      name = 'cassorm',
      version = __version__,
      author = 'John Wehr',
      author_email = 'johnwehr@gmail.com',
      maintainer = 'John Wehr',
      maintainer_email = 'johnwehr@gmail.com',
      description = 'Django ORM for use with Apache Cassandra',
      url = 'https://github.com/wehriam/cassorm/',
      download_url = 'https://github.com/wehriam/cassorm/tarball/master',
      keywords = 'cassandra client db distributed thrift pycassa django',
      packages = ['cassorm'],
      py_modules = ['ez_setup'],
      requires = ['pycassa'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.4',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules'
          ]
      )