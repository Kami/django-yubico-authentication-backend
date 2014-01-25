# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import re
from setuptools import setup

version_re = re.compile(
    r'__version__ = (\(.*?\))')

cwd = os.path.dirname(os.path.abspath(__file__))
fp = open(os.path.join(cwd, 'django_yubico', '__init__.py'))

version = None
for line in fp:
    match = version_re.search(line)
    if match:
        version = eval(match.group(1))
        break
else:
    raise Exception('Cannot find version in __init__.py')
fp.close()

setup(
    name='django_yubico',
    version='.' . join(map(str, version)),
    description='Yubico Yubikey authentication backend for Django',
    author='Tomaz Muraus',
    author_email='tomaz+pypi@tomaz.me',
    license='BSD',
    url='http://github.com/Kami/django-yubico-authentication-backend/',
    packages=['django_yubico'],
    install_requires=[
        'yubico-client>=1.9,<1.10'
    ],
    provides=['django_yubico'],
    package_data={
        'django_yubico': [
            'site_media/images/*',
            'templates/django_yubico/*.html'
        ]
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries',
    ],
)
