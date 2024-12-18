project = "plone.api"
copyright = "2012, Plone Foundation"


# The suffix of source filenames.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

extensions = [
    "myst_parser",
    "sphinx_reredirects",
]
master_doc = "index"

# -- Options for MyST markdown conversion to HTML -----------------------------

myst_enable_extensions = [
    "linkify",  # Identify "bare" web URLs and add hyperlinks.
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "plone_sphinx_theme"


# -- sphinx-reredirects configuration ----------------------------------
# https://documatt.com/sphinx-reredirects/usage.html
redirects = {
    "index": "https://6.docs.plone.org/plone.api/index.html",
}

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
