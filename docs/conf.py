from importlib.metadata import version

import sys


project = "plone.api"
copyright = "2012, Plone Foundation"

version = release = version("plone.api")


# The suffix of source filenames.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]
master_doc = "index"

locale_dirs = ["translated/"]
language = "en"

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual])
# This enables PDF generation.
latex_documents = [
    (
        "index",
        "ploneapi.tex",
        "plone.api Documentation",
        "",
        "manual",
    )
]


class Mock:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        if name in ("__file__", "__path__"):
            return "/dev/null"
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        else:
            return Mock()


MOCK_MODULES = ["lxml"]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()


# -- Options for MyST markdown conversion to HTML -----------------------------

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "linkify",  # Identify "bare" web URLs and add hyperlinks.
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "plone_sphinx_theme"


# -- Intersphinx configuration ----------------------------------

# This extension can generate automatic links to the documentation of objects
# in other projects. Usage is simple: whenever Sphinx encounters a
# cross-reference that has no matching target in the current documentation set,
# it looks for targets in the documentation sets configured in
# intersphinx_mapping. A reference like :py:class:`zipfile.ZipFile` can then
# linkto the Python documentation for the ZipFile class, without you having to
# specify where it is located exactly.
#
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
#
# Note that Plone Documentation imports documentation from several remote repositories.
# These projects need to build their docs as part of their CI/CD and testing.
# We use Intersphinx to resolve targets when either the individual project's or
# the entire Plone Documentation is built.
intersphinx_mapping = {
    "plone": ("https://6.docs.plone.org/", None),  # for imported packages
    "plone5": ("https://5.docs.plone.org/", None),
}
