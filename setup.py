from setuptools import setup, find_packages

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1a2'

setup(
    name='plone.api',
    version=version,
    description='A Plone API.',
    long_description=read('README.rst'),
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
        'Plone',  # this is needed so we can pull docstrings into Sphinx
        'zope.location<4.0.0',  # needed so autodoc can import
    ],
    extras_require={
        'develop': [
            'Sphinx',
            'manuel',
            'pep8',
            'setuptools-flakes',
        ],
        'test': [
            'plone.app.dexterity',
            'plone.app.testing',
            'mock',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    platforms='Any',
)
