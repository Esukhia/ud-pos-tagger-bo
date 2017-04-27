#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pytib',
    version='0.0.0',
    description="PyTib contains a Python3 module to process Tibetan text. It segments text into words, checks for spelling mistakes and more.",
    long_description=readme + '\n\n' + history,
    author="Drupchen Dorje",
    author_email='hhdrupchen@gmail.com',
    url='https://github.com/drupchen/pytib',
    packages=[
        'pytib',
    ],
    package_dir={'pytib':
                 'pytib'},
    entry_points={
        'console_scripts': [
            'pytib=pytib.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pytib',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
