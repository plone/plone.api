from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read("README.md") + "\n\n" + read("CHANGES.rst") + "\n\n" + read("LICENSE")
)

version = "2.0.0a4"

setup(
    name="plone.api",
    version=version,
    description="A Plone API.",
    long_description=long_description,
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    license="GPL version 2",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    url="https://github.com/plone/plone.api",
    keywords="plone api",
    install_requires=[
        "Products.statusmessages",
        "decorator",
        "plone.app.uuid",
        "plone.app.linkintegrity",
        "plone.uuid",
        "setuptools",
        "zope.globalrequest",
    ],
    extras_require={
        "test": [
            "Products.CMFPlone",
            "manuel>=1.11.2",
            "plone.app.dexterity",
            "plone.app.intid",
            "plone.app.testing",
            "plone.indexer",
            "plone.registry",
            "z3c.relationfield",
            "zope.testrunner",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    platforms="Any",
)
