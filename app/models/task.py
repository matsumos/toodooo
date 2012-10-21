#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from formencode import validators, compound, Schema
from ..models.basemodel import BaseModel

class TaskSchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = compound.All(
        validators.UnicodeString(not_empty=True),
        validators.MaxLength(255)
    )
    description = validators.UnicodeString()

class Task(BaseModel):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    doned_at = Column(DateTime)

    schema = TaskSchema

