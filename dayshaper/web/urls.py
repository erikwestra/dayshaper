""" dayshaper.web.urls

    This module defines the URLs used by the "web" application.
"""
from django.conf.urls import *

#############################################################################

urlpatterns = []
urlpatterns += patterns('dayshaper.web.views',
    (r'^$',                              'main.main'),
    (r'^plan/$',                         'plan.list'),
    (r'^plan/(?P<parent_id>\d+)/$',      'plan.list'),
    (r'^plan/add/$',                     'plan.add'),
    (r'^plan/add/(?P<parent_id>\d+)/$',  'plan.add'),
    (r'^plan/edit/(?P<task_id>\d+)/$',   'plan.edit'),
    (r'^plan/delete/(?P<task_id>\d+)/$', 'plan.delete'),
    (r'^do/$',                           'do.suggest_task'),
    (r'^do/(?P<task_id>\d+)/$',          'do.do_task'),
    (r'^reflect/$',                      'reflect.reflect'),
)

