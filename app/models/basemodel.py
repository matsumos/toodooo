#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, scoped_session
from shimehari.configuration import ConfigManager
from sqlalchemy import func
from formencode import Invalid
from inflector import Inflector
import copy

inflector = Inflector()

config = ConfigManager.getConfig()
url = config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(url, encoding='utf-8')
session = scoped_session(sessionmaker(autoflush=True, bind=engine))

class Model(object):

    @declared_attr
    def __tablename__(cls):
        return inflector.tableize(cls.__name__)

    id =  Column(Integer, primary_key=True)

    # accessibleAttributes = ()

    errors = {}
    query = None

    def __init__(self):
        self.validatorSchema = None

    def updateAttributes(self, attributes):
        print attributes
        for key, value in attributes.iteritems():
            # mass assignment 対策
            # if not key in self.accessibleAttributes:
               # continue

            if isinstance(getattr(self, key), list):
                if hasattr(getattr(self, key), '_sa_adapter'):

                    table_name = getattr(self, key)._sa_adapter._key

                    component_path = str("app.models.%s" % inflector.classify(table_name)).split('.')
                    package_path   = component_path[:-1]
                    package_name   = ".".join(package_path)
                    class_name     = component_path[-1]

                    __import__(str(package_name))
                    import sys
                    cls = getattr(sys.modules[package_name],class_name)

                    string_value = value

                    value = []
                    for val in string_value:
                        value.append(session.query(cls).get(val))
            else:
                if hasattr(self, key + '_id'):
                    if value == '':
                        value = None
                    setattr(self, key + '_id', value)
                    continue

            # print key, value
            setattr(self, key, value)
        self.save()

    def validate(self, attributes):
        self.errors = {}
        try:
            return self.validatorSchema.to_python(attributes)
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
