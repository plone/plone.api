from setuptools import setup, find_packages

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('docs','README.rst') + \
    read('docs','CHANGES.rst') + \
    read('docs', 'LICENSE.txt')

version = '1.2.0'

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
        'setuptools',
        'Plone',
        'decorator',
    ],
    extras_require={
        'develop': [
            'coverage',
            'flake8',
            'jarn.mkrelease',
            'manuel',
            'Sphinx',
            'zest.releaser',
        ],
        'test': [
            'manuel',
            'mock',
            'plone.app.dexterity',
            'plone.app.testing',
            'unittest2',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.0',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    platforms='Any',
)
