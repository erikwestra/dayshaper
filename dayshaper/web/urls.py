""" dayshaper.web.urls

    This module defines the URLs used by the "web" application.
"""
from django.conf.urls import *

#############################################################################

urlpatterns = []
urlpatterns += patterns('dayshaper.web.views',
    (r'^$',                     'main.main'),
    (r'^plan/$',                'plan.plan'),
    (r'^plan/list/$',           'plan.list'),
    (r'^plan/load/$',           'plan.load'),
    (r'^plan/save/$',           'plan.save'),
    (r'^plan/add_sibling/$',    'plan.add_sibling'),
    (r'^plan/add_child/$',      'plan.add_child'),
    (r'^plan/delete/$',         'plan.delete'),
    (r'^plan/move/$',           'plan.move'),
    (r'^do/$',                  'suggest.suggest'),
    (r'^do/(?P<task_id>\d+)/$', 'do.do'),
    (r'^reflect/$',             'reflect.reflect'),
    (r'^prefs/$',               'prefs.prefs'),
)

