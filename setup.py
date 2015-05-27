#!/usr/bin/env python

import os
import sys

version = "0.3.8"

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist register upload")
    sys.exit(1)

# These are required because sometimes PyPI refuses to bundle certain files
try:
    long_desc = open('README').read()
except:
    long_desc = ""

try:
    license = open('LICENSE.txt').read()
except:
    license = "Apache 2.0 License"

PY2 = sys.version_info < (3,)
PY3 = not PY2

setup(
    name='gnippy',
    version=version,
    description='Python library for GNIP.',
    long_description=long_desc,
    author='Abhinav Ajgaonkar',
    author_email='abhinav316@gmail.com',
    packages=['gnippy'],
    url='http://pypi.python.org/pypi/gnippy/',
    license=license,
    install_requires=[
        # Since this was explicitly requested for in older version, keep
        # it as is. Use the latest requests for PY3
        "requests == 1.2.0" if PY2 else "requests"
    ]
)
