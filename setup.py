#!/usr/bin/env python

from setuptools import setup


setup(
    name='ExtendedDateTimeFormat',
    version='0.1.0',
    author='Joseph Liechty',
    author_email='joeyliechty@gmail.com',
    packages=['ExtendedDateTimeFormat'],
    url='http://pypi.python.org/pypi/ExtendedDateTimeFormat/',
    license='LICENSE.txt',
    description='Extended Date Time Format Validation',
    long_description=open('README.md').read(),
    install_requires=[
        "pyparsing",
        "argparse",
        "datetime",
    ],
)
