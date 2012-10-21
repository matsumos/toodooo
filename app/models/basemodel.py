#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import session
from sqlalchemy import func
from formencode import Invalid
import copy

class BaseModel(object):

    accessibleAttributes = ()

    errors = {}

    def __init__(self):
        self.schema = None

    @classmethod
    def query(cls):
        return session.query(cls)

    def updateAttributes(self, attributes):
        for key, value in attributes.iteritems():
            # mass assignment 対策
            # if not key in self.accessibleAttributes:
               # continue
            setattr(self, key, value)
        self.save()

    def validate(self, attributes):
        self.errors = {}
        try:
            return self.schema.to_python(attributes)
        except Invalid, e:
            self.errors.update(e.error_dict)
            raise

    def save(self):
        try:
            session.add(self)
            session.commit()
        except:
            session.rollback()
            raise

    def copy(self):
        return copy.deepcopy(self)

    def delete(self):
        try:
            if hasattr(self, "deleted_at"):
                self.deleted_at = func.now()
            else:
                session.delete(self)
            session.commit()
        except:
            session.rollback()
            raise
