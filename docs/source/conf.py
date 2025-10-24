# -- Configuration du projet -----------------------------------------------------
import os
import sys
import django

sys.path.insert(0, os.path.abspath('../..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')
django.setup()

project = 'OC Lettings Site'
copyright = '2025, Elvis'
author = 'Elvis'
release = '1.0.0'

# -- Extensions Sphinx -----------------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options HTML ---------------------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
