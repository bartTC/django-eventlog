#!/usr/bin/env python
from setuptools import find_packages, setup

long_description = u'\n\n'.join((
    open('README.rst').read(),
    open('CHANGELOG.rst').read()
))

setup(
    name='django-eventlog',
    version='0.1a',
    description='django-eventlog stores event messages in a Django model.',
    long_description=long_description,
    author='Martin Mahner',
    author_email='martin@mahner.org',
    url='https://github.com/bartTC/django-eventlog/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    packages=find_packages(),
    package_data={
        # 'eventlog': ['templates/*.*'],
        # 'docs': ['*'],
    },
    include_package_data=True,
    install_requires=[
        'django>=1.8',
        'six',
    ],
    extras_require={
        'tests': []
    },
)
