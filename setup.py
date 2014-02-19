#!/usr/bin/env python
# coding: utf-8

import os
import sys
from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

from setuptools.command.test import test as TestCommand


# testing with py.test and `setup.py test`
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')
requirements = open('requirements/production.txt').readlines()


setup(
    name='budgetApp',
    version='0.1.0',

    description='Application to keeping your budget right',
    long_description=readme + '\n\n' + history,
    author='Piotr Banaszkiewicz',
    author_email='piotr@banaszkiewicz.org',
    url='https://github.com/pbanaszkiewicz/budgetApp',

    packages=find_packages(),
    package_dir={'budgetApp': 'budgetApp'},
    include_package_data=True,
    install_requires=requirements,

    license="MIT",
    zip_safe=False,
    keywords='budget',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'PyPI :: NoUpload',
    ],
    tests_require=['pytest'],
    cmdclass={
        'test': PyTest
    },
)
