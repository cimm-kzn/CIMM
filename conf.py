from os.path import abspath
from sys import path
path.insert(0, abspath('.'))

from pybtex.plugin import register_plugin
from gost import GOSTStyle


project = 'CIMM'
copyright = '2020, Kazan Chemoinformatics and Molecular Modeling Lab'
author = 'Ramil Nugmanov'
release = '2020.01.17'

extensions = ['recommonmark', 'sphinx_rtd_theme', 'sphinxcontrib.bibtex', 'sphinxcontrib.images']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = 'imgs/logo.jpg'
html_favicon = 'imgs/favicon.ico'
html_show_copyright = True
html_show_sphinx = False
html_show_sourcelink = False
html_scaled_image_link = False

html_css_files = [
    'style.css',
]

html_sidebars = {
    '**': [
        'globaltoc.html'
    ]
}

html_theme_options = {
    'canonical_url': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': None,
    'style_external_links': True,
    'style_nav_header_background': 'white',

    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
    'analytics_id': 'UA-72457412-1'
}


register_plugin('pybtex.style.formatting', 'gost_style', GOSTStyle)

images_config = {
    'override_image_directive': True
}
