#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Antoine Veuiller'
SITENAME = AUTHOR
SITEURL = 'https://aveuiller.github.io'
THEME = 'themes/plumage'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PATH = 'content'
OUTPUT_PATH = 'output'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (('Twitter', 'http://twitter.com/AVeuiller'),
          ('StackOverflow', 'https://stackoverflow.com/users/2564085/aveuiller'),
          ('GitHub', 'http://github.com/aveuiller'),
          ('Medium', 'https://aveuiller.medium.com/'),)

DEFAULT_PAGINATION = 10


# Custom Home page
# DIRECT_TEMPLATES = (('index', 'tags', 'categories'))
DIRECT_TEMPLATES = ["index", "tags", "categories", "authors", "archives", "search"]
