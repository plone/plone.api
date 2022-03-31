# sphinx configuration

project = 'plone.api'
copyright = '2012, Plone Foundation'

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
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

from pkg_resources import get_distribution
version = release = get_distribution(project).version

import sys


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


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

