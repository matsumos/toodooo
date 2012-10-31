#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from formencode import validators, compound, Schema
from ..models.basemodel import BaseModel

class MilestoneSchema(Schema):
    allow_extra_fields = True
    # filter_extra_fields = True
    name = compound.All(
        validators.UnicodeString(not_empty=True),
        validators.MaxLength(255)
    )

class Milestone(BaseModel):
    name = Column(String(255))

    validatorSchema = MilestoneSchema

