#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
from os import path
import codecs
import os
import re
import sys


# When creating the sdist, make sure the django.mo file also exists:
if 'sdist' in sys.argv or 'develop' in sys.argv:
    try:
        os.chdir('fluent_comments')
        # from django.core.management.commands.compilemessages import Command
        # Command.compile_messages(sys.stderr)
    finally:
        os.chdir('..')


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")

install_requires=[
    'django-crispy-forms>=1.1.1',
    'django-tag-parser>=2.1',
]

if sys.version_info[0] >= 3:
    # Akismet 0.2 does not support Python 3.
    if 'install' in sys.argv or 'develop' in sys.argv:
        print("\nwarning: skipped Akismet as dependency because it does not have a Python 3 version.")
else:
    install_requires += [
        'akismet>=0.2',
        'django-contrib-comments>=1.5',
    ]

setup(
    name='django-fluent-comments',
    version=find_version('fluent_comments', '__init__.py'),
    license='Apache 2.0',

    install_requires=install_requires,
    requires=[
        'Django (>=1.3)',   # Using staticfiles
    ],
    extras_require = {
        'threadedcomments': ['django-threadedcomments>=1.0b1'],
    },
    description='A modern, ajax-based appearance for django_comments',
    long_description=read('README.rst'),

    author='Diederik van der Boor',
    author_email='opensource@edoburu.nl',

    url='https://github.com/edoburu/django-fluent-comments',
    download_url='https://github.com/edoburu/django-fluent-comments/zipball/master',

    packages=find_packages(exclude=('example*',)),
    include_package_data=True,

    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Framework :: Django',
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
