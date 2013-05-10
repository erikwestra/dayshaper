""" dayshaper.web.views.reflect

    This view implements the various view functions for the "reflect" mode for
    the Dayshaper system.
"""
import datetime

from django.http      import HttpResponse
from django.shortcuts import render

from dayshaper.shared.lib import activities, utils

#############################################################################

def reflect(request):
    """ Respond to the "/reflect" URL.

        This is the main view for the "reflect" mode.
    """
    # Calculate a summary of the tasks worked on over the past 7 days.

    started_at = utils.start_of_day() - datetime.timedelta(days=7)
    ended_at   = utils.current_datetime()

    weekly_summary = activities.calc_task_summary(started_at, ended_at)

    # Now calculate a summary for each day of the week, grouping the results by
    # day and storing the results in a format which makes it easy for us to
    # generate the final table.

    day_start = started_at
    day_end   = started_at + datetime.timedelta(days=1) \
              - datetime.timedelta(seconds=1)

    daily_task_times = [] # List of times spent on the various tasks each day.
                          # For each day, the list item will be a dictionary
                          # with the following entries:
                          #
                          #     'day_label'
                          #
                          #         The label to use to identify this day.
                          #
                          #     'task_times'
                          #
                          #         A dictionary mapping each Task record ID to
                          #         the time spent on that task, as an integer
                          #         number of seconds.

    start_of_today = utils.start_of_day()
    while day_start <= start_of_today:
        weekday = day_start.date().weekday()
        day_label = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                     "Saturday", "Sunday"][weekday]

        daily_summary = activities.calc_task_summary(day_start, day_end)

        def _add_task_times(daily_summary, task_times):
            """ Recursively add 'daily_summary' to the 'task_times' dictionary.
            """
            for node in daily_summary:
                task_times[node['task'].id] = node['time_spent']
                _add_task_times(node['children'], task_times)

        task_times = {}
        _add_task_times(daily_summary['summary'], task_times)

        daily_task_times.append({'day_label'  : day_label,
                                 'task_times' : task_times})

        day_start = day_start + datetime.timedelta(days=1)
        day_end   = day_end   + datetime.timedelta(days=1)

    daily_task_times.reverse() # Show newest day first.

    # Process the weekly task summary, building a master list of all tasks
    # worked on during the week.

    tasks = [] # List of tasks worked on during the week.  Each list item is a
               # dictionary with the following entries:
               #
               #     'task'
               #
               #         The Task object to work on.
               #
               #     'label'
               #
               #         The (possibly indented) label to use for this task.
               #
               #     'time_spent'
               #
               #         The total amount of time spent on this task over the
               #         last week, as an integer number of seconds.

    def _add_tree(tree, task, indent=0):
        """ Recursively add a summary tree to the list of tasks.
        """
        for node in tree:
            label = "&nbsp;" * indent * 8 + node['task'].label
            tasks.append({'task'       : node['task'],
                          'label'      : label,
                          'time_spent' : node['time_spent']})

            _add_tree(node['children'], tasks, indent=indent+1)

    _add_tree(weekly_summary['summary'], tasks)

    # Calculate the totals to display at the bottom of the table.

    weekly_total = 0 # Total time spent for the week, in seconds.
    for task in tasks:
        weekly_total = weekly_total + task['time_spent']

    daily_totals = [] # Total time spent per day, in seconds.
    for day in daily_task_times:
        daily_total = 0
        for task_time in day['task_times'].values():
            daily_total = daily_total + task_time
        daily_totals.append(daily_total)

    # Using the calculated information, build a single large table representing
    # the entire summary.

    summary_table = [] # List of [col][row] entries.  Each list item is a
                       # dictionary with the following entries:
                       #
                       #    'text'
                       #
                       #        The text to be displayed.
                       #
                       #    'style'
                       #
                       #        The CSS style to apply to this table item.

    # Add the heading row to the top of the table.

    row = []
    row.append({'text'  : "&nbsp;",
                'style' : "heading"})
    row.append({'text'  : "Last 7 Days",
                'style' : "heading border-b"})
    row.append({'text'  : "&nbsp;",
                'style' : "heading"})

    for day in daily_task_times:
        row.append({'text'  : day['day_label'],
                    'style' : "heading border-b"})

    summary_table.append(row)

    # Add each task in turn.

    for task in tasks:
        row = []
        row.append({'text'  : task['label'] + "&nbsp;&nbsp;",
                    'style' : "heading left"})
        row.append({'text'  : utils.seconds_to_hms(task['time_spent']),
                    'style' : "body border-lrb"})
        row.append({'text'  : "&nbsp;",
                    'style' : "body"})

        task_id = task['task'].id
        for day in daily_task_times:
            if task_id in day['task_times']:
                task_time = utils.seconds_to_hms(day['task_times'][task_id])
            else:
                task_time = "&nbsp;"

            row.append({'text'  : task_time,
                        'style' : "body border-lrb"})

        summary_table.append(row)

    # Add the total times to the bottom of the table.

    row = []
    row.append({'text'  : "&nbsp;",
                'style' : "heading right"})
    row.append({'text'  : utils.seconds_to_hms(weekly_total),
                'style' : "body border-t"})
    row.append({'text'  : "&nbsp;",
                'style' : "body"})

    for daily_total in daily_totals:
        row.append({'text'  : utils.seconds_to_hms(daily_total),
                    'style' : "body border-t"})

    summary_table.append(row)

    # Finally, display the table to the user.

    return render(request, "reflect.html",
                  {'table' : summary_table})

