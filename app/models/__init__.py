#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from shimehari.configuration import ConfigManager
from sqlalchemy import *
from sqlalchemy.orm import *

config = ConfigManager.getConfig()
url = config['SQLALCHEMY_DATABASE_URI'] + '?charset=utf8'
engine = create_engine(url, encoding='utf-8')

session = scoped_session(sessionmaker(autoflush=True, bind=engine))

declarative_base = declarative_base(engine)

from .task import Task
