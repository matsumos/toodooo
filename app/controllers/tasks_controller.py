#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shimehari import request, Response, ApplicationController, flash, redirect
from werkzeug.exceptions import abort
from ..helpers import paged
from app.models import Task
from jinja2_form_extension.helpers import parse_form_data as parseFromData

class TasksController(ApplicationController):
    def __init__(self, name):
        ApplicationController.__init__(self, name)

    #Create your controller here.

    PER_PAGE = 5

    def index(self, page=1):
        tasks = Task.query.filter(Task.doned_at == None).order_by(Task.created_at.desc())
        tasks, pagination = paged(page, self.PER_PAGE, tasks)
        return self.renderTemplate('tasks/index.slim', tasks=tasks, pagination=pagination)

    def search(self, query='', page=1):
        tasks = Task.query.filter(Task.doned_at == None).order_by(Task.created_at.desc())
        tasks = tasks.filter(Task.name.like('%' + query + '%'))
        tasks, pagination = paged(page, self.PER_PAGE, tasks)
        return self.renderTemplate('tasks/index.slim', tasks=tasks, pagination=pagination)

    def show(self, id):
        task = Task.query.get(id)
        if not task:
            abort(404)
        return self.renderTemplate('tasks/show.slim', task=task)

    def edit(self, id):
        task = Task.query.get(id)
        if not task:
            abort(404)
        return self.renderTemplate('tasks/edit.slim', task=task)

    def new(self, *args, **kwargs):
        task = Task()
        return self.renderTemplate('tasks/new.slim', task=task)

    def create(self, *args, **kwargs):
        task = Task()
        params = parseFromData(request.form.copy())
        try:
            validParams = task.validate(params['task'])
            task.updateAttributes(validParams)
            flash(u'新規作成しました。', 'success')
            return redirect('/tasks/%s' % task.id)
        except:
            flash(u'保存に失敗しました。', 'error')

            #うーむ...
            task = task.copy()
            for key, value in params['task'].iteritems():
                setattr(task, key, value)

            return self.renderTemplate('tasks/edit.slim', task=task)

    def update(self, id):
        task = Task.query.get(id)
        params = parseFromData(request.form.copy())
        try:
            validParams = task.validate(params['task'])
            task.updateAttributes(validParams)
            flash(u'変更しました。', 'success')
            return redirect('/tasks/%s' % id)
        except:
            flash(u'保存に失敗しました。', 'error')

            #うーむ...
            task = task.copy()
            for key, value in params['task'].iteritems():
                setattr(task, key, value)

            return self.renderTemplate('tasks/edit.slim', task=task)

    def destroy(self, id):
        try:
            task = Task.query.get(id)
            task.delete()
            flash(u'削除しました。', 'success')
            return redirect('/tasks')
        except:
            flash(u'削除できませんでした。', 'error')
            return redirect('/tasks')
