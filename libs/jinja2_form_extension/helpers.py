#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parse_form_data(formData):
    rv = {}
    for key, value in formData.items():
        current = rv
        k = key.replace(']', '')
        bits = k.split('[')
        for bit in bits[:-1]:
            if bits[-1] != '':
                current = current.setdefault(bit, {})
            else:
                current = current.setdefault(bit, [])
        # Now assign value to current position
        try:
            if bits[-1] != '':
                current[bits[-1]] = value
            else:
                current += formData.getlist(key)
        except TypeError: # Special-case if current isn't a dict.
            current = {bits[-1]: value}
    return rv