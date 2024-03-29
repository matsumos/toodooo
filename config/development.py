#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from datetime import timedelta

DEBUG = True

# TEST = False

APP_DIRECTORY = 'app'
MAIN_SCRIPT = 'main'
# APP_INSTANCE_NAME = 'app'
# CONTROLLER_DIRECTORY = 'controllers'
# VIEW_DIRECTORY = 'views'
# ASSETS_DIRECTORY = 'assets'
STATIC_DIRECTORY = ['../static']
# MODEL_DIRECTORY = 'models'

# PREFERRED_URL_SCHEME = 'http'

# AUTO_SETUP = True

# CONTROLLER_AUTO_NAMESPACE = True

# TEMPLATE_ENGINE = 'jinja2'

SECRET_KEY = 'hogeeeeeeeeeeeeeee'

# SERVER_NAME = None

# PRESERVE_CONTEXT_ON_EXCEPTION = None
# PERMANENT_SESSION_LIFETIME = timedelta(days=31)
SESSION_COOKIE_NAME = '_toodooo_session'
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SECURE = False

# CACHE_STORE = None
# CACHE_DEFAULT_TIMEOUT = 300
# CACHE_THRESHOLD = 500
# CACHE_KEY_PREFIX = None
# CACHE_DIR = None
# CACHE_OPTIONS = None
# CACHE_ARGS = []

# LOG_FILE_OUTPUT = False
# LOG_FILE_ROTATE = False
# LOG_ROTATE_MAX_BITE = (5 * 1024 * 1024)
# LOG_ROTATE_COUNT = 5
# LOG_FILE_DIRECTORY = 'log'
LOG_DEBUG_FORMAT = '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s\n'
LOG_OUTPUT_FORMAT = '%(asctime)s %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s\n'

# DATABASE
import os
SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_POSTGRESQL_CHARCOAL_URL') or 'mysql://root@localhost/toodooo?charset=utf8'

# CSRF_EXPIRE = 1

DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
DEBUG_TB_PROFILER_ENABLED = True
DEBUG_TB_INTERCEPT_REDIRECTS = False