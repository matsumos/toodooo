#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
===============================
    Shimehari.core.manage.commands
    drink
    ~~~~~

    Shimehari App を起動します。

===============================
"""

import os
import sys
import threading
import traceback
from optparse import make_option

from shimehari.app import defaultHost, defaultPort
from shimehari.core.manage import AbstractCommand
from shimehari.core.helpers import importFromString
from shimehari.configuration import ConfigManager
from shimehari.core.exceptions import DrinkError


class Command(AbstractCommand):
    name = 'ds'
    summary = 'Present a web page at http://%s:%d/' % (defaultHost, defaultPort)
    usage = "Usage: %prog COMMAND [OPTIONS]"

    option_list = AbstractCommand.option_list + (
        make_option('--port', '-p', action='store', type='int', dest='port', default=8000, help='port number. default %default'),
        make_option('--host', action='store', type='string', dest='host', default=defaultHost, help='host name. default %default'),
        make_option('--browser', '-b', action='store_true', dest='browser', default=False, help='open browser.')
    )

    def __init__(self):
        super(Command, self).__init__()
        self.debug = False

    def run(self, *args, **options):
        import config

        # try:
        #     #humu-
        #     import config
        # except ImportError, e:
        #     sys.path.append(os.getcwd())
        #     try:
        #         import config
        #     except ImportError, e:
        #         t = sys.exc_info()[2]
        #         raise DrinkError(u'ちょっと頑張ったけどやっぱりコンフィグが見当たりません。\n%s' % e), None, traceback.print_exc(t)

        try:
            currentEnv = options.get('SHIMEHARI_ENV')
            currentConfig = ConfigManager.getConfig(currentEnv or 'development')
            app = importFromString( currentConfig['MAIN_SCRIPT'] + '.' + currentConfig['APP_INSTANCE_NAME'])

            if options.get('browser'):
                timer = threading.Timer(0.5, self.openBrowser, args=[self.host, self.port])
                timer.start()

            app.run(host=self.host, port=int(self.port), debug=True)

        except:
            raise
            # t = sys.exc_info()[2]
            # raise DrinkError(u'飲めるかと思ったのですが嘔吐しました。\n%s' % e), None, traceback.print_exc(t)

    def openBrowser(self, host, port):
        url = 'http://' + host + ':' + str(port)
        import webbrowser
        webbrowser.open(url)

    def handle(self, *args, **options):
        self.port = options.get('port')
        self.host = options.get('host')
        self.run(*args, **options)

Command()
