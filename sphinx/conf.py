import sys
import os
import time
import bottle

needs_sphinx = '8.0'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx',
              'sphinx.ext.ifconfig', 'sphinx.ext.viewcode']
locale_dirs = ['_locale/']
gettext_compact = False

master_doc = 'index'
project = u'Bottle'
copyright = u'2009-%s, %s' % (time.strftime('%Y'), bottle.__author__)
release = bottle.__version__
version = ".".join(release.split('-')[0].split(".")[:2])
language = 'en'

add_function_parentheses = True
add_module_names = False
autodoc_member_order = 'bysource'
autodoc_class_signature = 'separated'
intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
                       'werkzeug': ('https://werkzeug.palletsprojects.com/en/3.0.x', None)}

templates_path = ['templates']
pygments_style = 'sphinx'
html_theme = 'default'
html_style="bottle.css"
html_logo = "static/logo_nav.png"
html_favicon = "static/favicon.ico"
html_static_path = ['static']
html_last_updated_fmt = '%b %d, %Y'
html_use_smartypants = True
html_domain_indices = True
html_use_index = True
html_split_index = False
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True
html_sidebars = {
    'index': ['sidebar-intro.html', 'globaltoc.html', 'sidebar-releases.html', 'sidebar-links.html', 'searchbox.html'],
    '**':    ['sidebar-intro.html', 'localtoc.html', 'relations.html', 'sidebar-releases.html', 'sidebar-links.html', 'searchbox.html']
}

html_context = {
    'releases': []
}

with open('../releases.txt') as fp:
    for line in fp:
        if line.startswith('#'): continue
        branch, slug, name = line.strip().split(None, 2)
        html_context["releases"].append((branch, slug, name))

