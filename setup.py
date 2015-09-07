# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + \
    read('docs', 'CHANGES.rst') + \
    read('docs', 'LICENSE.txt')

version = '1.4.1'

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
            'unittest2',
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
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    platforms='Any',
)
