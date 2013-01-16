#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shimehari import request, Response, ApplicationController, flash, redirect
from werkzeug.exceptions import abort
from ..helpers import paged
from app.models import *
from jinja2_form_extension.helpers import parse_form_data as parseFromData
from formencode import Invalid


class TasksController(ApplicationController):

    def __init__(self, name):
        ApplicationController.__init__(self, name)

    #Create your controller here.

    PER_PAGE = 5

    def index(self, page=1):
        tasks = Task.query.filter(Task.doned_at == None).order_by(Task.created_at.desc())
        tasks, pagination = paged(page, self.PER_PAGE, tasks)
        tags = Tag.query.order_by(Tag.name)
        return self.renderTemplate('tasks/index.slim', tasks=tasks, pagination=pagination, tags=tags, action='index')

    def dones(self, page=1):
        tasks = Task.query.filter(Task.doned_at != None).order_by(Task.doned_at.desc())
        tasks, pagination = paged(page, self.PER_PAGE, tasks)
        return self.renderTemplate('tasks/index.slim', tasks=tasks, pagination=pagination, action='done')

    def search(self, query='', page=1):
        tasks = Task.query.filter(Task.doned_at == None).order_by(Task.created_at.desc())
        tasks = tasks.filter(Task.name.like('%' + query + '%'))
        tasks, pagination = paged(page, self.PER_PAGE, tasks)
        return self.renderTemplate('tasks/index.slim', tasks=tasks, pagination=pagination, query=query)

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

    def done(self, id):
        task = Task.query.get(id)
        task.done()
        flash(u'タスクを完了しました。', 'success')
        return redirect(request.environ.get("HTTP_REFERER"))

    def undone(self, id):
        task = Task.query.get(id)
        task.undone()
        flash(u'タスクを未完了にしました', 'success')
        return redirect(request.environ.get("HTTP_REFERER"))

    def new(self, *args, **kwargs):
        task = Task()
        return self.renderTemplate('tasks/new.slim', task=task)

    def create(self, *args, **kwargs):
        task = Task()
        params = parseFromData(request.form.copy())
        try:
            validParams = task.validate(params['task'])
            task.update(validParams)
            flash(u'新規作成しました。', 'success')
            return redirect('/tasks/%s' % task.id)
        except Invalid, e:
            flash(u'保存に失敗しました。', 'error')
            return self.renderTemplate('tasks/edit.slim', task=task, errors=e.error_dict, params=params)

    def update(self, id):
        task = Task.query.get(id)
        params = parseFromData(request.form.copy())
        try:
            validParams = task.validate(params['task'])
            task.update(validParams)
            flash(u'変更しました。', 'success')
            return redirect('/tasks/%s' % id)
        except Invalid, e:
            flash(u'保存に失敗しました。', 'error')
            return self.renderTemplate('tasks/edit.slim', task=task, errors=e.error_dict, params=params)

    def destroy(self, id):
        try:
            task = Task.query.get(id)
            task.delete()
            flash(u'削除しました。', 'success')
            return redirect('/tasks')
        except:
            flash(u'削除できませんでした。', 'error')
            return redirect('/tasks')
