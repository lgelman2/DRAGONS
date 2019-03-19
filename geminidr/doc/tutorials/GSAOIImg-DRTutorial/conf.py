# -*- coding: utf-8 -*-
#
# <REPLACE-WITH-TITLE> documentation build configuration file, created 
# from team template.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# -- Setting up path to import modules ---------------------------------------
on_rtd = os.environ.get('READTHEDOCS') == 'True'

print(' Printing current working directory for debugging:')
print(' ' + os.getcwd())

if on_rtd:
    sys.path.insert(0, os.path.abspath('./../../../'))
else:
    sys.path.insert(0, os.path.abspath('./../../../'))


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'


# -- Project information -----------------------------------------------------
# General information about the project.

project = u'Tutorial Series - GSAOI Imaging Data Reduction with DRAGONS'
copyright = u'2019, Bruno C. Quint'
author = 'Bruno C. Quint'
# Note that AURA owns the Copyright, not you.

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = 'en'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'ReplaceWithTitle'


# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
  # The paper size ('letterpaper' or 'a4paper').
  #'papersize': 'letterpaper',

  # The font size ('10pt', '11pt' or '12pt').
  #'pointsize': '10pt',

  # Additional stuff for the LaTeX preamble.
  #'preamble': '',
  'preamble': '\usepackage{appendix} \setcounter{tocdepth}{0}',

  # This will remove blank pages.
  'classoptions': ',openany,oneside',
  'babel': '\\usepackage[english]{babel}',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index-latex', 'ReplaceWithTitle.tex', u'<REPLACE-WITH-TILE>',
   u'Your Name', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'replacewithtitle', u'<REPLACE-WITH-TITLE>',
     [u'Your Name'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'ReplaceWithTitle', u'<REPLACE-WITH-TITLE>',
   u'Your Name', 'ReplaceWithTitle', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

intersphinx_mapping = {
    'astrodata': ('https://astrodata-user-manual.readthedocs.io/en/latest/', None),
    'astropy': ('http://docs.astropy.org/en/stable/', None),
    'gemini_instruments': ('https://astrodata-user-manual.readthedocs.io/en/latest/', None),
    'geminidr': ('https://dragons-recipe-system-programmers-manual.readthedocs.io/en/latest/', None),
    'matplotlib': ('http://matplotlib.sourceforge.net/', None),
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    'python': ('https://docs.python.org/3', None),
    'recipe_system': ('https://dragons-recipe-system-programmers-manual.readthedocs.io/en/latest/', None),
}

# Activate the todos
todo_include_todos=True


def run_api_doc(_):
    """
    Automatic API generator

    This method is used to generate API automatically by importing all the
    modules and sub-modules inside a package.

    It is equivalent to run:
    >>> sphinx-apidoc --force --no-toc --separate --module --output-dir api/ ../../ ../../cal_service

    It is useful because it creates .rst files on the file.

    NOTE
    ----
        This does not work with PyCharm default build. If you want to trigger
        this function, use the standard `$ make html` in the command line.
        The .rst files will be generated. After that, you can use PyCharm's
        build helper.
    """
    build_packages = [
        'geminidr'
    ]

    is_running_in_pycharm = "PYCHARM_HOSTED" in os.environ

    if is_running_in_pycharm:
        current_path = os.path.split(__file__)[0]
    else:
        current_path = os.getcwd()

    relative_path = "../../../../"

    print("Am I running on PyCharm? {}", is_running_in_pycharm)
    print("Current Path: {}", current_path)

    for p in build_packages:

        build_path = os.path.join(current_path, relative_path, p)

        ignore_paths = [
            'doc',
            'f2',
            'gmos',
            'gnirs',
            'niri',
            'test',
            'tests',
        ]

        ignore_paths = [os.path.join(build_path, i) for i in ignore_paths]

        argv = [
                   "--force",
                   "--no-toc",
                   # "--separate",
                   "--module",
                   "--output-dir", "api/",
                   build_path
               ] + ignore_paths

        sys.path.insert(0, build_path)

        try:
            # Sphinx 1.7+
            from sphinx.ext import apidoc
            apidoc.main(argv)

        except ImportError:
            # Sphinx 1.6 (and earlier)
            from sphinx import apidoc
            argv.insert(0, apidoc.__file__)
            apidoc.main(argv)


def setup(app):

    # Adding style in order to have the todos show up in a red box.
    app.add_stylesheet('todo-styles.css')
    app.add_stylesheet('code.xref-styles.css')

    # Automatic API generation
    app.connect('builder-inited', run_api_doc)
