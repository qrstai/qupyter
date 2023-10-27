# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Qupyter'
copyright = '2023, QRST AI'
author = 'QRST AI'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'myst_parser']
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']

html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    'icon_links': [
        {
            "name": "GitHub",
            "url": "https://github.com/qrstai/qupyter",
            "icon": "fa-brands fa-github",
        }
    ],
    'navbar_align': 'left',
    'logo': {
        'image_light': '/_static/qupyter-logo-black.png',
        'image_dark': '/_static/qupyter-logo-white.png',
    }
}

import os
import sys
sys.path.insert(0, os.path.abspath('../../.'))
sys.path.insert(0, os.path.abspath('../skeleton'))
