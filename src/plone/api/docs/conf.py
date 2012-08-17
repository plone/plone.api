# sphinx configuration

project = u'plone.api'
copyright = u'2012, Plone Foundation'

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]
master_doc = 'index'

# We define our own theme so we can have custom CSS that hides .. line-block::
# in Sphinx but still makes it visible on GitHub. This means that we can use
# .. line-block:: to display something only in GitHub and not on ReadTheDocs. */
html_theme = 'theme'
html_theme_path = ['.']

from pkg_resources import get_distribution
version = release = get_distribution(project).version
