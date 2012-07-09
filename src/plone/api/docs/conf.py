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

from pkg_resources import get_distribution
version = release = get_distribution(project).version
