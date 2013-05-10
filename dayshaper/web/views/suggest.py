""" dayshaper.web.views.suggest

    This view implements the "suggest" view for the Dayshaper system's "doing"
    mode.
"""
import datetime

from django.shortcuts import render

from dayshaper.shared.lib import activities, chooser, utils

#############################################################################

def suggest(request):
    """ Select a task and suggest that the user works on it.

        This is the main view for the "do" mode.
    """
    # Get the details of the most recently worked-on task, if any.

    activity = activities.latest_activity()
    if activity['task'] == None:
        recent_task = None
    else:
        age = utils.current_datetime() - activity['ended_at']
        if age > datetime.timedelta(hours=1):
            recent_task = None
        else:
            time_spent = \
                utils.format_seconds_for_display(activity['time_spent'])

            did_minimum = (activity['time_spent'] > activity['task'].min_time)

            recent_task = {'label'       : activity['task'].label,
                           'time_spent'  : time_spent,
                           'did_minimum' : did_minimum}

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

    suggested_task = chooser.choose_next_task()
    if suggested_task != None:
        start_url = "/do/" + str(suggested_task.id)
    else:
        start_url = None

    # Finally, display the suggested task to the user.

    total_time   = utils.format_seconds_for_display(summary['tot_time'])
    finished_url = "/"

    return render(request, "suggest.html",
                  {'recent_task'    : recent_task,
                   'task_table'     : task_table,
                   'total_time'     : total_time,
                   'suggested_task' : suggested_task,
                   'start_url'      : start_url,
                   'finished_url'   : finished_url})

