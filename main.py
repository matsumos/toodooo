#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('./libs/')

import config

from shimehari import Shimehari
from slimish_jinja import SlimishExtension
from webassets.ext.jinja2 import AssetsExtension
from webassets import Environment as AssetsEnvironment
from webassets.loaders import YAMLLoader
from jinja2_decolater_extension import DecolaterExtension
from jinja2_form_extension import FormExtension

shimehariOptions = {
    'templateOptions': {
        'extensions': [
            SlimishExtension,
            AssetsExtension,
            DecolaterExtension,
            FormExtension
        ]
    }
}


app = Shimehari(__name__, **shimehariOptions)
app.templateEnv.authenticity_token_generator = app.templateEnv.globals['csrfToken']
app.templateEnv.authenticity_token_key = '_csrfToken'
# app.templateEnv.slim_debug = False
# app.templateEnv.slim_print = True


def setupAssetEnviromentFromYAML(app, yamlFile):
    appDir = './' + app.config['APP_DIRECTORY'] + '/'
    assetEnv = AssetsEnvironment(appDir, '/')
    bundles = YAMLLoader(appDir + yamlFile).load_bundles()
    for bundle in bundles:
        assetEnv.register(bundle, bundles[bundle])
    app.templateEnv.assets_environment = assetEnv
setupAssetEnviromentFromYAML(app, 'assets/bundles.yml')

# from shimehari_debugtoolbar import DebugToolbarExtension

# toolbar = DebugToolbarExtension(app)

# from shimehari.configuration import ConfigManager
# isDebug = ConfigManager.getConfig().get('DEBUG', False)
# if isDebug:
#     from werkzeug.debug import DebuggedApplication
#     app = DebuggedApplication(app, evalex=True)

# if __name__ == '__main__':
#     app.drink()
