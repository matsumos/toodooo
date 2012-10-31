#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import nodes
from jinja2.ext import Extension
from .form_record import FormRecord
from .constants import *

class FormExtension(Extension):

    DEFAULT_FORM_BLOCK_ASSIGNEE = intern('f')

    # a set of names that trigger the extension.
    tags = set([
        'form_for',
        'string',
        'input',
        'label',
        'button',
        'textarea',
        'boolean',
        'checkboxes',
        'radiobuttons',
        'select',
        'file',
        'hidden',
        'password'
        'tel',
        'email',
        'search',
        'url',
        'association'
    ])

    def __init__(self, environment):
        super(FormExtension, self).__init__(environment)

        # add the defaults to the environment
        environment.extend(
            use_html5=True,
            required_text='required',
            required_mark='*',
            authenticity_token_generator=None,
            authenticity_token_key='authenticity_token'
        )

    def parse(self, parser):
        tag = parser.stream.next()
        parse_method = getattr(self, '_parse_%s_tag' % tag.value)
        return parse_method(parser, tag)

    def _parse_form_for_tag(self, parser, tag):
        lineno = tag.lineno
        
        class_attr = self._pasrse_short_class_attr(parser)
            
        record = parser.parse_expression()

        arguments = [record]

        arguments += self._parse_keyword_args(parser, support_with_statement=True)

        if class_attr:
            arguments.append(class_attr)

        if parser.stream.current.test('name'):
            assignee = parser.parse_expression().name
        else:
            assignee = self.DEFAULT_FORM_BLOCK_ASSIGNEE

        body = parser.parse_statements(['name:end' + tag.value], drop_needle = True)
        
        self._skip_after_block_end(parser)

        return nodes.CallBlock(
            self.call_method('_exec_' + tag.value, arguments),
            [nodes.Name(assignee, 'store')],
            [],
            body
        ).set_lineno(lineno)

    def _exec_form_for(self, record, **kwargs):
        caller = kwargs['caller']

        form_attributes = kwargs
        del form_attributes['caller']

        record = FormRecord(record)
        record.use_html5 = self.environment.use_html5
        record.required_text = self.environment.required_text
        record.required_mark = self.environment.required_mark
        record.authenticity_token_generator = self.environment.authenticity_token_generator
        record.authenticity_token_key = self.environment.authenticity_token_key

        return record.form(caller, **form_attributes)

    def _common_parse(f):
        def decorator(self, parser, tag):
            lineno = tag.lineno
            
            class_attr = self._pasrse_short_class_attr(parser)
                
            arguments = f(self, parser, tag)

            arguments += self._parse_keyword_args(parser)

            if class_attr:
                arguments.append(class_attr)

            body = parser.parse_statements(['name:end' + tag.value], drop_needle = True)
            
            self._skip_after_block_end(parser)

            return nodes.CallBlock(
                self.call_method('_exec_' + tag.value, arguments),
                [],
                [],
                body
            ).set_lineno(lineno)
        return decorator

    @_common_parse
    def _parse_input_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_input(self, record, field_name, **kwargs):
        return record.input(field_name, **kwargs)

    @_common_parse
    def _parse_string_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_string(self, record, field_name, **kwargs):
        return record.string(field_name, **kwargs)

    @_common_parse
    def _parse_password_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_password(self, record, field, **kwargs):
        return record.password(field, **kwargs)

    @_common_parse
    def _parse_tel_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_tel(self, record, field, **kwargs):
        return record.tel(field, **kwargs)

    @_common_parse
    def _parse_email_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_email(self, record, field, **kwargs):
        return record.email(field, **kwargs)

    @_common_parse
    def _parse_search_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_search(self, record, field, **kwargs):
        return record.search(field, **kwargs)

    @_common_parse
    def _parse_url_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_url(self, record, field, **kwargs):
        return record.url(field, **kwargs)

    @_common_parse
    def _parse_file_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_file(self, record, field_name, **kwargs):
        return record.file(field_name, **kwargs)

    @_common_parse
    def _parse_hidden_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_hidden(self, record, field_name, **kwargs):
        return record.hidden(field_name, **kwargs)

    @_common_parse
    def _parse_label_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_label(self, record, field, label_text=None, **kwargs):
        return record.label(field, label_text, **kwargs)

    @_common_parse
    def _parse_boolean_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_boolean(self, record, field, label_text=None, **kwargs):
        return record.boolean(field, label_text, **kwargs)

    @_common_parse
    def _parse_textarea_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_textarea(self, record, field, label_text=None, **kwargs):
        return record.textarea(field, label_text, **kwargs)

    @_common_parse
    def _parse_select_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        options = parser.parse_expression()
        return [record, field_name, options]

    def _exec_select(self, record, field, options, **kwargs):
        return record.select(field, options, **kwargs)

    @_common_parse
    def _parse_radiobuttons_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        options = parser.parse_expression()
        return [record, field_name, options]

    def _exec_radiobuttons(self, record, field, options, **kwargs):
        return record.radiobuttons(field, options, **kwargs)

    @_common_parse
    def _parse_checkboxes_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        options = parser.parse_expression()
        return [record, field_name, options]

    def _exec_checkboxes(self, record, field, options, **kwargs):
        return record.checkboxes(field, options, **kwargs)

    @_common_parse
    def _parse_association_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_association(self, record, field, **kwargs):
        return record.association(field, **kwargs)

    @_common_parse
    def _parse_button_tag(self, parser, tag):
        record = parser.parse_expression()
        field_name = nodes.Const(parser.stream.expect('name').value)
        return [record, field_name]

    def _exec_button(self, record, button_type=None, button_text=None, **kwargs):
        return record.button(button_type, button_text, **kwargs)

    def _pasrse_short_class_attr(self, parser):
        class_attrs = []
        
        while parser.stream.current.test('dot'):
            parser.stream.expect('dot')
            class_attrs.append(parser.stream.current.value)
            parser.stream.skip()

        # jinja タグの中では class キーワードが使えないため cls で代用
        rv = nodes.Keyword(CLASS_KEYWORD_ALIAS, nodes.Const(" ".join(class_attrs)))
        
        return rv

    def _parse_keyword_args(self, parser, support_with_statement=False):
        rv = []

        while parser.stream.current.type is not 'block_end':
            # skip colon for python compatibility
            if parser.stream.skip_if('colon'):
                break

            if parser.stream.skip_if('block_end'):
                break

            if support_with_statement:
                if parser.stream.skip_if('name:with'):
                    break

            parser.stream.skip_if('comma')

            if parser.stream.current.test('name') and parser.stream.look().test('assign'):
                name = parser.stream.next().value
                parser.stream.skip()
                value = parser.parse_expression()
                rv.append(nodes.Keyword(name, value))
            else:
                rv.append(parser.parse_expression())
        return rv

    def _skip_after_block_end(self, parser):
        # slimish jinja 対策
        while parser.stream.current.test('dot'):
            parser.stream.expect('dot')
            parser.stream.skip()
