""" dayshaper.web.views.do

    This view implements the various view functions for the "do" mode for
    the Dayshaper system.
"""
import datetime
import time

from django.http      import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils     import timezone

from dayshaper.shared.models import *
from dayshaper.shared.lib    import activities, chooser, utils

#############################################################################

def suggest_task(request):
    """ Select a task and suggest that the user works on it.

        This is the main view for the "do" mode.

            Parent 1 -> Leaf Node 1
            Parent 1 -> Leaf Node 2
            Parent 2 -> Leaf Node 3
    """
    # Calculate the summary of the tasks worked on so far today.

    started_at = utils.start_of_day() #.replace(day=17)
    ended_at   = utils.current_datetime()

    summary = activities.calc_task_summary(started_at, ended_at)

    # Convert the task tree into a "table" of nested activities.

    task_table = []

    def _add_tree(tree, task_table, indent=0):
        """ Recursively add the tree to the task table.
        """
        for node in tree:
            time_spent = utils.format_seconds_for_display(node['time_spent'])
            indent_str = "&nbsp;" * 8
            task_table.append({'task'       : node['task'],
                               'time_spent' : time_spent,
                               'prefix'     : indent_str * indent})
            _add_tree(node['children'], task_table, indent=indent+1)

    _add_tree(summary['summary'], task_table)

    # Choose the suggested task to work on next.

    total_time     = utils.format_seconds_for_display(summary['tot_time'])
    suggested_task = chooser.choose_next_task()
    start_url      = "/do/" + str(suggested_task.id)
    finished_url   = "/"

    return render(request, "suggest.html",
                  {'task_table'     : task_table,
                   'total_time'     : total_time,
                   'suggested_task' : suggested_task,
                   'start_url'      : start_url,
                   'finished_url'   : finished_url})

#############################################################################

def do_task(request, task_id):
    """ Respond to the user doing the given task.

        We display a page where the user can click on "Finished" to finish the
        task.  We then return back to the main "suggest" page.
    """

    if request.method == "POST":

        # Respond to the user clicking on one of our "Submit" buttons.

        if request.POST.get("cancel") != None:
            # The user cancelled -> redirect back to the "suggest" view.
            return HttpResponseRedirect("/do")

        if request.POST.get("finished") != None:
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

    return render(request, "do.html",
                  {'suggested_task' : suggested_task,
                   'start_time'     : start_time,
                   'suggested_time' : suggested_time})

