# sphinx configuration

project = u'plone.api'
copyright = u'2012, Plone Foundation'

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

# Use-case: we want to display a warning message that is only visible on GitHub
# and not on ReadTheDocs. We achieve this by adding a custom CSS that hides
# .. line-block:: in Sphinx but still makes it visible on GitHub because GitHub
# does not load this custom CSS. line-block was chosen because it's deprecated
# and shouldn't be used anymore anyhow
html_static_path = ['static']


def setup(app):
    app.add_stylesheet('lineblock.css')


from pkg_resources import get_distribution
version = release = get_distribution(project).version
