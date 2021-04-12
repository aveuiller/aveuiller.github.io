#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import plumage
THEME = plumage.get_path()
PLUGINS = [
    "pelican_webassets",
]


AUTHOR = 'Antoine Veuiller'
SITENAME = AUTHOR
SITEURL = 'http://localhost:8000'
RELATIVE_URLS = False

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

CODE_STYLE = "emacs"
MARKDOWN = {
    "extension_configs": {
        "pymdownx.highlight": {
            "linenums": True,
            "linenums_style": "pymdownx-inline",
            "noclasses": True
        },
        "pymdownx.superfences": {
            "disable_indented_code_blocks": True,
        },
    },
}

# Custom Home page
DIRECT_TEMPLATES = ["index", "tags", "categories", "authors", "archives", "search"]
