#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, scoped_session
from shimehari.configuration import ConfigManager
from sqlalchemy import func
from formencode import Invalid
import copy

config = ConfigManager.getConfig()
url = config['SQLALCHEMY_DATABASE_URI'] + '?charset=utf8'
engine = create_engine(url, encoding='utf-8')
session = scoped_session(sessionmaker(autoflush=True, bind=engine))

class Model(object):

    # accessibleAttributes = ()

    errors = {}
    query = None

    def __init__(self):
        self.schema = None

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


def session_mapper(cls):
    cls.query = session.query(cls)


class BaseDeclarativeMeta(DeclarativeMeta):
    def __init__(cls, classname, bases, dict_):
        DeclarativeMeta.__init__(cls, classname, bases, dict_)
        if not Model in bases:
            session_mapper(cls)


BaseModel = declarative_base(engine, metaclass=BaseDeclarativeMeta, cls=Model)
