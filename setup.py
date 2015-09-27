# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + '\n\n' + \
    read('docs', 'CHANGES.rst') + '\n\n' + \
    read('docs', 'LICENSE.txt')

version = '1.4.7'

setup(
    name='plone.api',
    version=version,
    description='A Plone API.',
    long_description=long_description,
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    license='GPL version 2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/plone/plone.api',
    keywords='plone api code conventions',
    install_requires=[
        'Products.statusmessages',
        'decorator',
        'plone.app.uuid',
        'plone.uuid',
        'setuptools',
        'zope.globalrequest',
    ],
    extras_require={
        'develop': [
            'Sphinx',
            'coverage',
            'flake8',
            'jarn.mkrelease',
            'manuel',
            'zest.releaser',
        ],
        'test': [
            'Products.CMFPlone',
            'manuel',
            'mock',
            'plone.app.dexterity',
            'plone.app.testing',
            'plone.indexer',
            'plone.registry',
        ],
        'archetypes': [
            'Products.Archetypes',
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    platforms='Any',
)
