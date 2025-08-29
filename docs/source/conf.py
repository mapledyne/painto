# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..\\..', 'src'))

project = 'painto'
copyright = '2025, Michael Knowles'
author = 'Michael Knowles'
release = '0.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

autosummary_generate = True
autodoc_member_order = 'bysource'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'nature'
html_static_path = ['_static']

html_scaled_image_link = False



rst_epilog = """
.. |painto| replace:: **🌈painto**
.. |red| image:: ../assets/FF0000.png
.. |blue| image:: ../assets/0000FF.png
.. |green| image:: ../assets/00FF00.png
"""

def list_hex_assets():
    """List files in ../assets/ that match hex color code PNGs (RRGGBB.png)."""
    import re
    assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
    hex_pattern = re.compile(r'^[0-9A-Fa-f]{6}\.png$')
    try:
        files = os.listdir(assets_dir)
    except FileNotFoundError:
        return []
    matches = [fname.replace(".png", "") for fname in files if hex_pattern.match(fname)]
    return matches

for hex in list_hex_assets():
    asset = f".. |{hex}| image:: ../assets/{hex}.png\n"
    rst_epilog += asset

print(rst_epilog)