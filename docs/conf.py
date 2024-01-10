# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'proggyleg'
copyright = '2024, Johnnie Gray'
author = 'Johnnie Gray'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

extensions = [
    'myst_nb',
]

# msyt_nb configuration
nb_execution_mode = "auto"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "hsl(144, 80%, 30%)",
        "color-brand-content": "hsl(144, 80%, 30%)",
    },
    "dark_css_variables": {
        "color-brand-primary": "hsl(144, 70%, 40%)",
        "color-brand-content": "hsl(144, 70%, 40%)",
    },
}

html_static_path = ['_static']
html_css_files = ["my-styles.css"]