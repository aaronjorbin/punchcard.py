#!/usr/bin/env python

from distutils.core import setup

version = "0.1"
setup(name='punchcard.py',
      version=version,
      description='Command line utility to create a punchcard graph',
      author='Aaron Jorbin',
      author_email='aaron@jorb.in',
      url='http://github.com/aaronjorbin/punchcard.py',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
            'Topic :: Terminals',
            ],
      download_url="http://github.com/downloads/aaronjorbin/punchcard/punchcard.py-%s.tar.gz" % version,
      scripts = ['punchcard/punchcard.py']
     )
