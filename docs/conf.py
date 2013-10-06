# sphinx configuration
     
html_domain_indices = False
html_output_encoding = 'utf-8' # hardcoded special char &reg; (®) added to Plone®
html_show_sourcelink = False
html_use_index = False
html_logo = "plone-logo-48.png"
html_sidebars = { '**': [ 'globaltoc.html' ]  }

project = u'plone.api'
copyright = u'2013, Plone Foundation'
source_encoding = 'utf-8' # index.rst has special Plone&right; character
extensions = []
#extensions = [
#    'sphinx.ext.doctest',
#    'sphinx.ext.coverage',
#    'sphinx.ext.autodoc',
#    'sphinx.ext.viewcode',
#    'sphinx.ext.autosummary',
#]
master_doc = 'index'

locale_dirs = ["translated/"]
language = 'en'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual])
# This enables PDF generation.
latex_documents = [(
    'index',
    'ploneapi.tex',
    u'plone.api Documentation',
    u'', 'manual'
), ]

# Use-case: we want to display a warning message that is only visible on GitHub
# and not on ReadTheDocs. We achieve this by adding a custom CSS that hides
# .. line-block:: in Sphinx but still makes it visible on GitHub because GitHub
# does not load this custom CSS. line-block was chosen because it's deprecated
# and shouldn't be used anymore anyhow
html_static_path = ['static']

exclude_patterns = ['_build']



def setup(app):
    app.add_stylesheet('lineblock.css')


# version = release = get_distribution(project).version
version = release = ''

import sys


class Mock(object):
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
