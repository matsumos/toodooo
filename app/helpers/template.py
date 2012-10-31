#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2_decolater_extension import templateMethod, templateFilter

from shimehari import request
from shimehari.helpers import urlFor

@templateMethod
def urlForOtherPage(page):
    args = request.viewArgs.copy()
    args['page'] = page
    return urlFor(request.endpoint, **args)


from datetime import datetime

@templateFilter
def timeSince(dt, past_="ago", 
    future_="from now", 
    default="just now"):
    """
    Returns string representing "time since"
    or "time until" e.g.
    3 days ago, 5 hours from now etc.
    """

    now = datetime.utcnow()
    if now > dt:
        diff = now - dt
        dt_is_past = True
    else:
        diff = dt - now
        dt_is_past = False

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s %s" % (period, \
                singular if period == 1 else plural, \
                past_ if dt_is_past else future_)

    return default


from shimehari import getFlashedMessage

@templateMethod
def getFlashedMessages(*args,**kwargs):
    return getFlashedMessage(*args,**kwargs)


from jinja2.runtime import Undefined

@templateFilter
def altImage(value, alternative):
    if value == None or value == '' or isinstance(value, Undefined):
        return '/assets/images/default-%s.gif' % alternative
    return value


@templateMethod
def backPath():
    referrer = request.environ.get("HTTP_REFERER") or 'javascript:history.back()'
    return referrer

