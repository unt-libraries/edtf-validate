#!/usr/bin/env python

from setuptools import setup


setup(
    name='edtf-validate',
    version='2.0.0',
    author='Mark Phillips',
    author_email='mark.phillips@unt.edu',
    packages=['edtf_validate'],
    url='https://github.com/unt-libraries/edtf-validate',
    license='BSD',
    entry_points={
        'console_scripts': ['edtf-validate=edtf_validate.valid_edtf:main'],
    },
    description='Extended Date Time Format Validation',
    long_description='See the home page for more information.',
    install_requires=[
        "pyparsing",
        "argparse",
        "datetime",
    ],
    keywords=['edtf', 'extended', 'datetime', 'validate'],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
