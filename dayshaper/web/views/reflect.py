""" dayshaper.web.views.reflect

    This view implements the various view functions for the "reflect" mode for
    the Dayshaper system.
"""
from django.http import HttpResponse

#############################################################################

def reflect(request):
    """ Respond to the "/reflect" URL.

        This is the main view for the "reflect" mode.
    """
    # Calculate a summary of the tasks worked on so far this week.

    started_at = utils.start_of_week()
    ended_at   = utils.curent_datetime()

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
                          #         the time spent on that task, as a string
                          #         formatted for display.

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
                time_spent = \
                    utils.format_seconds_for_display(node['time_spent'])
                task_times[node['task'].id] = time_spent
                _add_task_times(node['children'], task_times)

        task_times = {}
        _add_task_times(daily_summary['summary'], task_times)

        daily_task_times.append({'day_label'  : day_label,
                                 'task_times' : task_times})

        day_start = day_start + datetime.timedelta(days=1)
        day_end   = day_end   + datetime.timedelta(days=1)

    daily_task_times.reverse() # Show newest day first.

    # Process the weekly task summary, building a master list of all tasks
    # worked on during the week, and the total amount of time spent on each
    # task.

    task_names        = []
    weekly_task_times = []

    def _add_tree(tree, task_names, weekly_task_times, indent=0):
        """ Recursively add a summary tree to the given lists.
        """
        time_spent = utils.format_seconds_for_display(node['time_spent'])
        indent_str = "&nbsp;" * 8
        task_names.append(indent_str * indent + node['task'].label)
        weekly_task_times.append(time_spent)
        _add_tree(node['children'], task_names, weekly_task_times,
                  indent=indent+1)

    _add_tree(weekly_summary['summary'], task_names, weekly_task_times)

    # Using the calculated information, build a single large table to be
    # displayed.

    row_headings = []
    

#################

    # Convert the summary trees into a single meta-table to be displayed.

    daily_task_times = [] # List of times spent on each task each day.  The
                          # index into this list matches the index into the
                          # 'daily_summaries' 

    row_headings = [] # Heading to use for each row in the table.
    col_headings = [] # Heading to use for each column in the table.
    contents     = [] # Nested list of [col][row] values.  Each value is a
                      # dictionary with the following entries:
                      #
                      #     'text'
                      #
                      #         The text to display in this cell in the table.
                      #
                      #     '

    return HttpResponse("More to come...")

