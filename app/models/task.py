#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from formencode import validators, compound, Schema
from ..models.basemodel import BaseModel

class TaskSchema(Schema):
    allow_extra_fields = True
    # filter_extra_fields = True
    name = compound.All(
        validators.UnicodeString(not_empty=True),
        validators.MaxLength(255)
    )
    description = validators.UnicodeString()
    tags = validators.Set()
    milestone = validators.Int()

TasksTags = Table('tasks_tags', BaseModel.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Task(BaseModel):

    name = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    doned_at = Column(DateTime)
    tags = relationship("Tag", secondary=TasksTags, backref="tasks")
    milestone_id = Column(Integer, ForeignKey('milestones.id'))
    milestone = relationship("Milestone", backref="tasks")

    validatorSchema = TaskSchema

    def done(self):
        self.doned_at = func.now()
        self.save()

    def undone(self):
        self.doned_at = None
        self.save()