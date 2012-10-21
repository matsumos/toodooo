#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
===============================
    [[Shimehari Config]]
    config
    ~~~~~~

===============================
"""

from shimehari.configuration import Config, ConfigManager
from werkzeug.utils import import_string
from shimehari.helpers import getEnviron

currentEnv = getEnviron()

obj = import_string('config.%s' % currentEnv)
config = {}
for key in dir(obj):
    if key.isupper():
        config[key] = getattr(obj, key)

ConfigManager.addConfig(Config(currentEnv, config))
