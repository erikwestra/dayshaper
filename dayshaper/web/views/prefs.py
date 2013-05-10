""" dayshaper.web.views.prefs

    This view implements the view functions for the "preferences" mode for the
    Dayshaper system.
"""
import datetime

from django.http      import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from dayshaper.shared.lib    import preferences
from dayshaper.shared.models import *

#############################################################################

def prefs(request):
    """ Respond to the "/prefs" URL.

        This is the main view for the "prefs" mode.
    """
    if request.method == "GET":
        # We're displaying the form for the first time.  Set up our defaults.

        err_msg  = None
        strategy = preferences.get_int("TOP_LEVEL_STRATEGY")

    elif request.method == "POST":
        # Get the entered form values.

        if request.POST.get("cancel") != None:
            # The user cancelled -> return to the main page.
            return HttpResponseRedirect("/")

        err_msg = None # initially.

        strategy = request.POST.get("strategy")
        if strategy == None:
            err_msg = "You must select a strategy."

        if err_msg == None:
            preferences.set_int("TOP_LEVEL_STRATEGY", strategy)
        return HttpResponseRedirect("/")

    # If we get here, display the preferences form.

    return render(request, "prefs.html",
                  {'strategy_choices' : Task.STRATEGY_CHOICES,
                   'err_msg'          : err_msg,
                   'strategy'         : strategy})

