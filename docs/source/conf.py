# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import datetime
from importlib.metadata import PackageNotFoundError, version as _version

# No sys.path fiddling: autodoc and the builder both use the installed
# sphinx-docx. The checkout carries no generated sphinx_docx/docx/style.docx,
# so putting it first on sys.path breaks every build that does not set
# docx_style -- which is what the CI docx build hit.

# -- Project information -----------------------------------------------------

project = 'sphinx-docx'
author = 'Nefti-sama'
copyright = '2019 amedama41, 2022-%s %s' % (datetime.date.today().year, author)

try:
    release = _version('sphinx-docx')
except PackageNotFoundError:  # building from a source tree, not installed
    release = '0.0.0.dev0'
version = '.'.join(release.split('.')[:2])

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx_docx',
    'sphinx.ext.autodoc',
    'sphinx.ext.graphviz',
    'sphinx.ext.mathjax',
]

autodoc_member_order = 'bysource'
math_number_all = True
numfig = True
numfig_secnum_depth = 2

source_suffix = {'.rst': 'restructuredtext'}
master_doc = 'index'
language = 'en'
exclude_patterns = []
pygments_style = 'monokai'

# -- Options for docx output -------------------------------------------------

docx_documents = [
    ('index', 'sphinx_docx.docx', {
        'title': project,
        'creator': author,
        'subject': 'Sphinx builder extension',
        'keywords': ['Sphinx', 'sphinx-docx', 'Office Word'],
        'publishDate': datetime.date.today(),
        'version': release,
    }, True),
]
docx_pagebreak_before_file = 1
docx_table_options = {'row_splittable': False}

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

# -- Options for LaTeX output ------------------------------------------------

latex_documents = [
    (master_doc, 'sphinx_docx.tex', 'sphinx-docx', author, 'manual'),
]
