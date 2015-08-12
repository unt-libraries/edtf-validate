#!/usr/bin/env python

from setuptools import setup


setup(
    name='edtf-validate',
    version='0.1.0',
    author='Mark Phillips',
    author_email='mark.phillips@unt.edu',
    packages=['edtf_validate'],
    url='http://pypi.python.org/pypi/edtf-validate/',
    license='LICENSE.txt',
    description='Extended Date Time Format Validation',
    long_description=open('README.md').read(),
    install_requires=[
        "pyparsing",
        "argparse",
        "datetime",
    ],
)
