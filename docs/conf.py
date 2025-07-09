#!/usr/bin/env python3
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import sys

pkg_root = os.path.join(os.path.dirname(__file__), '../')
sys.path.insert(0, pkg_root)
print(sys.path[0])
# sys.path.insert(0, os.path.abspath('.'))
from mypielib.version import VERSION

# General information about the project.
project = 'mypielib'
copyright = '2025, Alejandro Liu'
author = 'Alejandro Liu'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = VERSION
# The full version, including alpha/beta/rc tags.
# release = '0.0.0'

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'autodoc2',
    'myst_parser',
    'sphinxarg.ext',
    'sphinx.ext.doctest',
    ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

autodoc2_packages = [
  '../mypielib',
]
autodoc2_render_plugin = 'myst'
autodoc2_sort_names = True
autodoc2_hidden_objects = {'inherited','private'}

myst_enable_extensions = [
    'fieldlist',
    'linkify',
    'substitution',
    'strikethrough',
]
myst_substitutions = {
  'version': version,
  'project': project,
  'copyright': copyright,
  'author': author,
}

# doctest_global_setup = '''
# import mypielib
# '''
# doctest_global_cleanup = '''
# del mypielib
# '''

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = '.rst'
source_suffix = [ '.rst', '.md' ]

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, project, f'{project} Documentation',
     [author], 1)
]
