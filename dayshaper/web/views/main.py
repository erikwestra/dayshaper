""" dayshaper.web.views.main

    This module defines the "main" view for the Dayshaper system.  This is the
    top-most URL used to access Dayshaper.
"""
from django.core.urlresolvers import reverse
from django.shortcuts         import render

#############################################################################

def main(request):
    """ Respond to the "/" URL.
    """
    return render(request, "main.html",
                  {'plan_url'    : "/plan",
                   'do_url'      : "/do",
                   'reflect_url' : "/reflect",
                   'prefs_url'   : "/prefs",
                  })

