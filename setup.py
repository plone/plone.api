from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "2.2.1"

long_description = (
    f"{Path('README.md').read_text()}\n"
    f"{Path('CHANGES.rst').read_text()}\n"
    f"{Path('LICENSE').read_text()}"
)

setup(
    name="plone.api",
    version=version,
    description="A Plone API.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
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
    python_requires=">=3.8",
    install_requires=[
        "Products.statusmessages",
        "Products.PlonePAS",
        "Products.CMFPlone",
        "decorator",
        "plone.app.uuid",
        "plone.app.dexterity",
        "plone.app.intid",
        "plone.app.layout",
        "plone.app.linkintegrity",
        "plone.dexterity",
        "plone.i18n",
        "plone.registry",
        "plone.uuid",
        "setuptools",
        "zope.globalrequest",
        "Products.CMFCore",
        "z3c.relationfield",
        "zc.relation",
        "Zope",
        "zope.intid",
    ],
    extras_require={
        "test": [
            "borg.localrole",
            "manuel>=1.11.2",
            "plone.app.contenttypes",
            "plone.app.textfield",
            "plone.app.testing",
            "plone.testing",
            "plone.indexer",
            "plone.registry",
        ],
    },
    # Get more strings from
    # https://pypi.org/classifiers/
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    platforms="Any",
)
