#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import ceil

class Pagination(object):

    def __init__(self, currentPage, perPage, count):
        self.currentPage = currentPage
        self.perPage = perPage
        self.count = count

    @property
    def pages(self):
        return int(ceil(self.count / float(self.perPage)))

    @property
    def hasPrev(self):
        return self.currentPage > 1

    @property
    def hasNext(self):
        return self.currentPage < self.pages

    def iterPages(self, leftEdge=2, leftCurrent=2,
                   rightCurrent=5, rightEdge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= leftEdge or \
               (num > self.currentPage - leftCurrent - 1 and \
                num < self.currentPage + rightCurrent) or \
               num > self.pages - rightEdge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

def paged(page, per_page, session):
    pagemin = per_page * (page - 1)
    pagemax = per_page * page

    count = session.count()
    session = session[pagemin:pagemax]

    pagination = Pagination(page, per_page, count)

    return session, pagination
