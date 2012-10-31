#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .constants import *
from inflector import Inflector
from sqlalchemy.types import (
    # BIGINT,
    # BINARY,
    # BLOB,
    # BOOLEAN,
    # BigInteger,
    # Binary,
    Boolean,
    # CHAR,
    # CLOB,
    # DATE,
    # DATETIME,
    # DECIMAL,
    # Date,
    # DateTime,
    # Enum,
    # FLOAT,
    # Float,
    # INT,
    # INTEGER,
    Integer,
    # Interval,
    # LargeBinary,
    # NCHAR,
    # NVARCHAR,
    # NUMERIC,
    # Numeric,
    # PickleType,
    # REAL,
    # SMALLINT,
    # SmallInteger,
    String,
    TEXT,
    # TIME,
    # TIMESTAMP,
    Text,
    # Time,
    # TypeDecorator,
    # Unicode,
    # UnicodeText,
    # VARBINARY,
    VARCHAR,
    )

inflector = Inflector()

class FormRecord(object):

    record = None
    use_html5 = False
    required_text = ''
    required_mark = ''
    errors = {}
    columns_data = {}
    authenticity_token_generator = None
    authenticity_token_key = None

    def __init__(self, record = None):
        self.record = record
        model_name = self.record.__tablename__
        if record.id == None:
            self.action = '/%s' % model_name
            self.method = 'post'
        else:
            self.action = '/%s/%s' % (model_name, record.id)
            self.method = 'put'
        self.errors = self.record.errors
        # sqlalchemy
        self.columns_data = self.record.__table__.columns._data

    def _assign_classes(f):
        def decorator(self, *args, **attributes):
            if CLASS_KEYWORD_ALIAS in attributes:
                attributes.setdefault('class', attributes[CLASS_KEYWORD_ALIAS])
                del attributes[CLASS_KEYWORD_ALIAS]
            return f(self, *args, **attributes)
        return decorator

    def _assign_id(f):
        def decorator(self, *args, **attributes):
            field = args[0]
            attributes.setdefault('id', '%s_%s' % (inflector.singularize(self.record.__tablename__), field))
            return f(self, *args, **attributes)
        return decorator

    def _assign_for(f):
        def decorator(self, *args, **attributes):
            field = args[0]
            attributes.setdefault('for', '%s_%s' % (inflector.singularize(self.record.__tablename__), field))
            return f(self, *args, **attributes)
        return decorator

    def _assign_name(f):
        def decorator(self, *args, **attributes):
            field = args[0]
            attributes.setdefault('name', '%s[%s]' % (inflector.singularize(self.record.__tablename__), field))
            return f(self, *args, **attributes)
        return decorator

    def _render_attributes(self, attributes):
        if 'caller' in attributes:
            del attributes['caller']
        rv = ''
        for attribute, value in attributes.items():
            rv += ' %s="%s"' % (attribute, value or '')
        return rv

    @_assign_classes
    def form(self, caller, **attributes):
        if not 'method' in attributes:
            attributes['method'] = 'post'
        else:
            self.method = attributes['method']
            attributes['method'] = 'post'

        attributes.setdefault('action', self.action)
        attributes.setdefault('accept-charset', 'UTF-8')

        inner = ''
        inner += '<div style="margin:0;padding:0;display:inline">'
        if self.authenticity_token_key and self.authenticity_token_generator:
            inner += '<input name="%s" type="hidden" value="%s">' % (self.authenticity_token_key, self.authenticity_token_generator())
        if self.method != 'post':
            inner += '<input name="_method" type="hidden" value="%s">' % self.method
        inner += '<input name="utf8" type="hidden" value="&#x2713;">'
        inner += '</div>'
        inner += caller(self)
        return '<form%s>%s</form>' % (self._render_attributes(attributes), inner)

    @_assign_for
    @_assign_classes
    def label(self, field, text = None, **attributes):
        if text == None:
            if 'caller' in attributes:
                text = attributes['caller']()

        required_text = ''
        # TODO: あとでやる

        if 'required' in attributes:
            if attributes['required'] == True:
                required_text = '<abbr title="%s">%s</abbr> ' % (self.required_text, self.required_mark)
            del attributes['required']
        
        return '<label%s>%s%s</label>' % (self._render_attributes(attributes), required_text, text)

    @_assign_id
    @_assign_name
    @_assign_classes
    def textarea(self, field, text = None, **attributes):

        if text is None:
            if 'caller' in attributes and attributes['caller'] != '':
                text = attributes['caller']()

        if text is None or not bool(text):
            text = getattr(self.record, field) or ''

        return '<textarea%s>%s</textarea>' % (self._render_attributes(attributes), text)

    @_assign_id
    @_assign_name
    @_assign_classes
    def boolean(self, field, text = None, **attributes):
        checked = ''
        if bool(getattr(self.record, field)):
            checked = ' checked="checked"'
        return '<input type="checkbox"%s%s>%s' % (self._render_attributes(attributes), checked, text)

    @_assign_classes
    def button(self, button_type='submit', text = None, **attributes):

        if text == None:
            if 'caller' in attributes:
                text = attributes['caller']()

        if button_type == None:
            button_type = 'submit'

        attributes.setdefault('type', button_type)

        if button_type == 'submit':
            attributes.setdefault('name', 'commit')

        return '<input%svalue="%s">' % (self._render_attributes(attributes), text)

    def _render_options(self, opts, value):
        rv = ''
        for option_value, option_text in opts.iteritems():
            if isinstance(option_text, dict):
                rv += '<optgroup label="%s">' % option_value
                rv += self._render_options(option_text, value)
                rv += '</optgroup>'
            else:
                selected = ''
                if value == option_value:
                    selected = ' selected="selected"'
                rv += '<option value="%s"%s>%s</option>' % (option_value, selected, option_text)
        return rv

    @_assign_id
    @_assign_name
    @_assign_classes
    def select(self, field, options, converted_value=None, **attributes):
        value = converted_value or getattr(self.record, field)

        rv = '<select%s>' % self._render_attributes(attributes)
        rv += '<option value=""></option>'
        rv += self._render_options(options, value)
        
        rv += '</select>'
        return rv

    @_assign_name
    def radiobuttons(self, field, options, converted_value=None, **attributes):
        value = converted_value or getattr(self.record, field)

        label_attributes = {}
        if CLASS_KEYWORD_ALIAS in attributes:
            label_attributes.setdefault('class', attributes[CLASS_KEYWORD_ALIAS])
            del attributes[CLASS_KEYWORD_ALIAS]

        rv = ''
        for option_value, option_text in options.iteritems():
            checked = ''
            if value == option_value:
                checked = ' checked="checked"'
            rv += '<label%s><input type="radio" value="%s"%s%s>%s</label>' % (self._render_attributes(label_attributes), option_value, checked, self._render_attributes(attributes), option_text)
        
        return rv

    @_assign_name
    def checkboxes(self, field, options, converted_values=None, **attributes):
        values = converted_values or getattr(self.record, field)

        label_attributes = {}
        if CLASS_KEYWORD_ALIAS in attributes:
            label_attributes.setdefault('class', attributes[CLASS_KEYWORD_ALIAS])
            del attributes[CLASS_KEYWORD_ALIAS]

        attributes['name'] += '[]'

        rv = ''
        rv = '<input name="%s" type="hidden" value="" />' % attributes['name']
        for option_value, option_text in options.iteritems():
            checked = ''
            if option_value in values:
                checked = ' checked="checked"'
            rv += '<label%s><input type="checkbox" value="%s"%s%s>%s</label>' % (self._render_attributes(label_attributes), option_value, checked, self._render_attributes(attributes), option_text)
        
        return rv
    

    def association(self, field, **attributes):

        from sqlalchemy.orm.properties import RelationshipProperty

        prop = self.record.__mapper__.get_property(field)

        if not isinstance(prop, RelationshipProperty):
            # TODO: あとでエラー出す
            raise

        direction = prop.direction.name

        from app.models import session

        options = {}
        for item in session.query(prop.mapper).all():
            options[item.id] = item.name

        if direction in ['MANYTOMANY', 'ONETOMANY']:
            converted_values = []
            for value in getattr(self.record, field):
                if not value is None:
                    converted_values.append(value.id)
            return self.checkboxes(field, options, converted_values, **attributes)

        elif direction == 'MANYTOONE':
            converted_value = None

            if not getattr(self.record, field) is None:
                converted_value = getattr(self.record, field).id

            return self.select(field, options, converted_value, **attributes)        

    @_assign_id
    @_assign_name
    @_assign_classes
    def string(self, field, **attributes):
        attributes.setdefault('value', getattr(self.record, field))

        return '<input type="text"%s>' % self._render_attributes(attributes)

    @_assign_id
    @_assign_name
    @_assign_classes
    def file(self, field, **attributes):
        attributes.setdefault('value', getattr(self.record, field))

        return '<input type="file"%s>' % self._render_attributes(attributes)

    @_assign_id
    @_assign_name
    @_assign_classes
    def tel(self, field, **attributes):
        attributes.setdefault('value', getattr(self.record, field))

        return '<input type="tel"%s>' % self._render_attributes(attributes)

    @_assign_id
    @_assign_name
    @_assign_classes
    def password(self, field, **attributes):
        attributes.setdefault('value', getattr(self.record, field))

        return '<input type="password"%s>' % self._render_attributes(attributes)

    @_assign_id
    @_assign_name
    @_assign_classes
    def email(self, field, **attributes):
        attributes.setdefault('value', getattr(self.record, field))

        return '<input type="email"%s>' % self._render_attributes(attributes)

    @_assign_id
    @_assign_name
    @_assign_classes
    def search(self, field, **attributes):
        attributes.setdefault('value', getattr(self.record, field))

        return '<input type="search"%s>' % self._render_attributes(attributes)

    @_assign_id
    @_assign_name
    @_assign_classes
    def url(self, field, **attributes):
        attributes.setdefault('value', getattr(self.record, field))

        return '<input type="url"%s>' % self._render_attributes(attributes)

    @_assign_id
    @_assign_name
    @_assign_classes
    def hidden(self, field, **attributes):
        attributes.setdefault('value', getattr(self.record, field))

        return '<input type="hidden"%s>' % self._render_attributes(attributes)

    def input(self, *args, **attributes):

        field = args[0]

        if not field in self.columns_data:
            return self.string(*args, **attributes)

        column = self.columns_data[field]

        # print column.type
        # print isinstance(column.type, String)
        # print isinstance(column.type, Text)

        if isinstance(column.type, Text):
            # attributes.setdefault('maxlength', 65535)
            return self.textarea(*args, **attributes)

        elif isinstance(column.type, String):
            attributes.setdefault('maxlength', column.type.length)
            return self.string(*args, **attributes)

        elif isinstance(column.type, Boolean):
            return self.boolean(*args, **attributes)

        elif isinstance(column.type, Integer):
            return self.string(*args, **attributes)

        else:
            return self.string(*args, **attributes)

    def get_value(self, name):
        return getattr(self.record, name)