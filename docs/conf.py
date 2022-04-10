from pkg_resources import get_distribution

import sys

project = 'plone.api'
copyright = '2012, Plone Foundation'

version = release = get_distribution(project).version


# The suffix of source filenames.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    "sphinx.ext.ifconfig",
    "myst_parser",
    "sphinx.ext.todo",
]
master_doc = 'index'

locale_dirs = ["translated/"]
language = 'en'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual])
# This enables PDF generation.
latex_documents = [(
    'index',
    'ploneapi.tex',
    'plone.api Documentation',
    '', 'manual'
), ]


def setup(app):
    app.add_config_value("plone_api_doctests", "", True)


class Mock:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        else:
            return Mock()


MOCK_MODULES = ['lxml']
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()


# -- Options for myST markdown conversion to html -----------------------------

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

