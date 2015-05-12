#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Yumminhuang'
SITENAME = u'/dev/null'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('NEU', 'https://www.northeastern.edu/'),
         ('JNU', 'http://www.jnu.edu.cn/'),
         ('Fionser\'s Blog', 'http://fionser.github.io/'), )

# Social widget
SOCIAL = (('github', 'http://github.com/yumminhuang'), (
    'stack-overflow', 'https://stackoverflow.com/users/2755574/yumminhuang'
), ('linkedin', 'http://www.linkedin.com/pub/yaming-huang/5b/932/6a0'),
          ('twitter', 'http://twitter.com/yumminhuang'),
          ('weibo', 'http://www.weibo.com/2622511625'),
          ('instagram', 'http://instagram.com/yumminhuang'), )
GITHUB_USER = 'yumminhuang'

DEFAULT_PAGINATION = 10

# Show modified date
SHOW_DATE_MODIFIED = 'True'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

BOOTSTRAP_NAVBAR_INVERSE = 'True'

# Enable TYPOGRIFY
# TYPOGRIFY = 'True'

# Blog theme
THEME = 'pelican-bootstrap3'
BOOTSTRAP_THEME = 'yeti'
# Code block style
PYGMENTS_STYLE = 'manni'
# Static path for pages, files, etc
# CUSTOM_CSS = 'theme/css/han.min.css'
STATIC_PATHS = ['images', 'static/han.min.css', ]
EXTRA_PATH_METADATA = {'static/han.min.css': {'path': 'theme/css/han.min.css'}}

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['cjk-auto-spacing']

# License
CC_LICENSE = 'CC-BY-NC'
