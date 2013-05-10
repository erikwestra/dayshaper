""" dayshaper.web.views.do

    This view implements the "do" view function for the Dayshaper system's
    "doing" mode.
"""
from django.http      import HttpResponseRedirect
from django.shortcuts import render

from dayshaper.shared.models import *
from dayshaper.shared.lib    import activities, utils

#############################################################################

def do(request, task_id):
    """ Respond to the user doing the given task.

        We display a page where the user can click on "Finished" to finish the
        task.  We then return back to the main "suggest" page.
    """

    if request.method == "POST":

        # Respond to the user clicking on one of our "Submit" buttons.

        button_clicked = request.POST.get("button_clicked")

        if button_clicked == "cancel":
            # The user cancelled -> redirect back to the "suggest" view.
            return HttpResponseRedirect("/do")

        if button_clicked == "finished":
            # The user clicked on the "Finished" button.  Record this activity,
            # and then go back to the "suggest" view.
            task       = Task.objects.get(id=task_id)
            seconds    = int(request.POST.get("start_time"))

            start_time = utils.seconds_to_datetime(seconds)
            end_time   = utils.current_datetime()

            activities.record_activity(task, start_time, end_time)

            return HttpResponseRedirect("/do")

    # If we get here, we're displaying the form for the first time.  Do so.

    suggested_task = Task.objects.get(id=task_id)
    start_time     = utils.datetime_to_seconds(utils.current_datetime())

    if suggested_task.min_time == suggested_task.max_time:
        suggested_time = "%d minutes" % suggested_task.min_time
    else:
        suggested_time = \
                "a minimum of %d minutes, and no more than %d minutes,"  % \
                (suggested_task.min_time, suggested_task.max_time)

    beep_time = suggested_task.min_time * 60 # Minutes -> seconds.

    return render(request, "do.html",
                  {'suggested_task' : suggested_task,
                   'start_time'     : start_time,
                   'suggested_time' : suggested_time,
                   'beep_time'      : beep_time})

