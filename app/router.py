#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shimehari import Router, Resource, Root
from werkzeug.routing import Rule
from controllers import TasksController

taskskController = TasksController('tasks')

appRoutes = Router([
    Root(taskskController.index),
    Resource(taskskController),
    Rule('/tasks/page/<int:page>', endpoint=taskskController.index),
    Rule('/tasks/search/<string:query>', endpoint=taskskController.search),
    Rule('/tasks/search/<string:query>/<int:page>', endpoint=taskskController.search)
])
