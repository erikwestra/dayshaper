""" dayshaper.urls

    This is the top-level URL configuration module for the Dayshaper system.
"""
from django.conf.urls import *
from django.conf      import settings

#############################################################################

# Start with an empty list of URL patterns.

urlpatterns = []

#############################################################################

# Set up the development server (only) to serve our static files.

if settings.SERVE_STATIC_MEDIA:
    urlpatterns += patterns('',
        (r'^assets/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root' : settings.STATICFILES_DIRS[0][1],
                 'show_indexes'  : True}),
    )

#############################################################################

# Include our various app-specific URLs.

urlpatterns += patterns('', (r'^/?', include('dayshaper.web.urls')))

