#
# DRAGONS Recipe System Programmer's Manual documentation build configuration file,
# sphinx-quickstart on Thu Mar 20 15:06:19 2014.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

# Adding configurations that are different on RTD or on local builds
on_rtd = os.environ.get('READTHEDOCS') == 'True'

print(' Printing current working directory for debugging:')
print((' ' + os.getcwd()))

if on_rtd:
    print(' Adding the following path to the sys.path')
    print((' ' + os.path.abspath('./../../../')))
    sys.path.insert(0, os.path.abspath('./../../../'))
else:
    sys.path.insert(0, os.path.abspath('./../../../'))


# -- Project information -----------------------------------------------------

project = "DRAGONS - Recipe System Programmer's Manual"
copyright = '2021, Association of Universities for Research in Astronomy'
author = 'Kenneth Anderson, Kathleen Labrie, Bruno Quint'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
version = '3.1'  # The short X.Y version.
release = '3.1.0-dev'  # The full version, including alpha/beta/rc tags.
#rtdurl = 'v'+release
#rtdurl = 'release-'+release
rtdurl = 'latest'


# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
   'sphinx.ext.autodoc',
   'sphinx.ext.intersphinx',
   'sphinx.ext.todo',
   'sphinx.ext.coverage',
   'sphinx.ext.imgmath',
   'sphinx.ext.ifconfig',
   'sphinx.ext.viewcode',
   'sphinx.ext.napoleon',
   'sphinx.ext.graphviz',
]


# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
today = 'December 2021'

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



# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = 'default'
#html_theme = 'sphinxdoc'
#html_theme = 'pyramid'

html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

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
htmlhelp_basename = 'RecipeSystemProgManual'

# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
    # This will remove blank pages.
    'classoptions': ',openany,oneside',
    'babel': '\\usepackage[english]{babel}',

    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
    'preamble': '\\usepackage{appendix} \\setcounter{tocdepth}{0}',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index-latex',
   'RecipeSystemProgManual.tex',
   "DRAGONS - Recipe System Programmer's Manual",
   'Kenneth Anderson, Kathleen Labrie, Bruno Quint', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = 'images/gemini_banner_poster.jpeg'
#latex_logo = 'images/black_gem.png'
latex_logo = 'images/GeminiLogo_new_2014.jpg'

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
    ('index',
     'recipesystemprogmanual',
     "DRAGONS - Recipe System Programmer's Manual",
     ['Kenneth Anderson, Kathleen Labrie, Bruno Quint'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index',
   'RecipeSystemProgManual',
   "DRAGONS - Recipe System Programmer's Manual",
   'Kenneth Anderson, Kathleen Labrie, Bruno Quint',
   'RecipeSystemProgManual',
   'Recipe System programming "how to"',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'


# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'astropy': ('http://docs.astropy.org/en/stable/', None),
    'python': ('https://docs.python.org/3', None),
}


# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Automatically generate API documentation --------------------------------

# -- Enable autoapi ----------------------------------------------------------
def run_api_doc(_):
    """
    Automatic API generator

    This method is used to generate API automatically by importing all the
    modules and sub-modules inside a package.

    It is equivalent to run:
    >>> sphinx-apidoc --force --no-toc --separate --module --output-dir api/ ../../ ../../cal_service

    It is useful because it creates .rst files on the fly.

    NOTE
    ----
        This does not work with PyCharm default build. If you want to trigger
        this function, use the standard `$ make html` in the command line.
        The .rst files will be generated. After that, you can use PyCharm's
        build helper.
    """
    build_packages = [
        # 'gempy',
        # 'geminidr',
        'recipe_system',
    ]

    is_running_in_pycharm = "PYCHARM_HOSTED" in os.environ

    if is_running_in_pycharm:
        current_path = os.path.split(__file__)[0]
    else:
        current_path = os.getcwd()

    relative_path = "../../../"

    print(("\n Am I running on PyCharm? {}".format(is_running_in_pycharm)))
    print((" Current Path: {}\n".format(current_path)))

    for p in build_packages:

        build_path = os.path.normpath(
            os.path.join(current_path, relative_path, p)
        )

        print(('\n Building API using the following build_path: {}\n'.format(
            build_path)))

        ignore_paths = [
            'doc',
            'test',
        ]

        ignore_paths = [os.path.join(build_path, i) for i in ignore_paths]
        api_path = os.path.normpath(os.path.join(current_path, 'api'))

        argv = [
                   "--force",
                   "--no-toc",
                   "--module",
                   "--output-dir", api_path,
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


# -- Finishing with a setup that will run always -----------------------------
def setup(app):

    # Adding style in order to have the todos show up in a red box.
    app.add_css_file('todo-styles.css')
    app.add_css_file('rtd_theme_overrides.css')
    app.add_css_file('css/custom_code.css')
    app.add_css_file('fonts.css')

    # Automatic API generation
    app.connect('builder-inited', run_api_doc)


rst_epilog = """
.. role:: raw-html(raw)
   :format: html

.. |caldb| replace:: :raw-html:`<a href="https://dragons-recipe-system-users-manual.readthedocs.io/en/{v}/caldb.html" target="_blank">caldb</a>`
.. |dataselect| replace:: :raw-html:`<a href="https://dragons-recipe-system-users-manual.readthedocs.io/en/{v}/supptools.html#dataselect" target="_blank">dataselect</a>`
.. |descriptors| replace:: :raw-html:`<a href="https://astrodata-user-manual.readthedocs.io/en/{v}/appendices/appendix_descriptors.html" target="_blank">descriptors</a>`
.. |descriptor| replace:: :raw-html:`<a href="https://astrodata-user-manual.readthedocs.io/en/{v}/appendices/appendix_descriptors.html" target="_blank">descriptors</a>`
.. |reduce| replace:: :raw-html:`<a href="https://dragons-recipe-system-users-manual.readthedocs.io/en/{v}/reduce.html" target="_blank">reduce</a>`
.. |showd| replace:: :raw-html:`<a href="https://dragons-recipe-system-users-manual.readthedocs.io/en/{v}/supptools.html#showd" target"_blank">showd</a>`
.. |showrecipes| replace:: :raw-html:`<a href="https://dragons-recipe-system-users-manual.readthedocs.io/en/{v}/supptools.html#showrecipes" target="_blank">showrecipes</a>`
.. |showpars| replace:: :raw-html:`<a href="https://dragons-recipe-system-users-manual.readthedocs.io/en/{v}/supptools.html#showpars" target="_blank">showpars</a>`
.. |typewalk| replace:: :raw-html:`<a href="https://dragons-recipe-system-users-manual.readthedocs.io/en/{v}/supptools.html#typewalk" target="_blank">typewalk</a>`
.. |atfile| replace:: :raw-html:`<a href="https://dragons-recipe-system-users-manual.readthedocs.io/en/{v}/reduce.html#the-file-facility" target="_blank">"at-file" Facility</a>`
.. |astrodatauser| replace:: :raw-html:`<a href="https://astrodata-user-manual.readthedocs.io/en/{v}/" target="_blank">Astrodata User Manual</a>`

.. |RSUser|  replace:: :raw-html:`<a href="http://dragons-recipe-system-users-manual.readthedocs.io/en/{v}/">Recipe System Users Manual</a>`
.. |astrodataprog| replace:: :raw-html:`<a href="https://astrodata-programmer-manual.readthedocs.io/en/{v}/">Astrodata Programmer Manual</a>`

""".format(v = rtdurl)
