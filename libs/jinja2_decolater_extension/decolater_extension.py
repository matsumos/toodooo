#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2.ext import Extension

class DecolaterExtension(Extension):

    environment = None
    methodPool = dict()
    filterPool = dict()

    def __init__(self, environment):
        super(DecolaterExtension, self).__init__(environment)

        self.environment = environment

        for method in self.methodPool:
           self.addTemplateMethod(self.methodPool[method], method) 
        for filter in self.filterPool:
           self.addTemplateFilter(self.filterPool[filter], filter) 

    @classmethod
    def templateMethod(self, name=None):
        def decorator(f):
            if self.environment == None:
                self.methodPool[name or f.__name__] = f
                return f
            self.addTemplateMethod(f, name=name)
            return f
        return decorator

    def addTemplateMethod(self, f, name):
        self.environment.globals[name or f.__name__] = f

    @classmethod
    def templateFilter(self, name=None):
        def decorator(f):
            # import pdb; pdb.set_trace()
            if self.environment == None:
                self.filterPool[name or f.__name__] = f
                return f
            self.addTemplateFilter(f, name=name)
            return f
        return decorator

    def addTemplateFilter(self, f, name):
        self.environment.filters[name or f.__name__] = f
