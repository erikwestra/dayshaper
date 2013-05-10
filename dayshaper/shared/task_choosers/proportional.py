""" dayshaper.shared.task_choosers.proportional

    This module implements the "proportional" task chooser for the Dayshaper
    system.  This chooses the next task so that tasks are worked on in
    proportion to their relative weighting.
"""
import datetime

from dayshaper.shared.models import *
from dayshaper.shared.lib    import activities, utils

#############################################################################

def choose_next_task(parent):
    """ Choose the next task to work on from among the given task's children.

        Upon completion, we return the Task object to work on next, or None if
        there are no active task objects.
    """
    # Build a list of the active tasks which have the given parent.

    tasks = []
    for task in Task.objects.filter(parent=parent, status=Task.STATUS_ACTIVE):
        tasks.append({'task' : task})

    # Calculate the latest activity for each task.

    for task in tasks:
        task['latest_activity'] = \
            activities.latest_activity_for_task(task['task'])

    # If any of these tasks has never been worked on, choose the first one.

    for task in tasks:
        if task['latest_activity'] == None:
            return task['task']

    # If we get here, every task has been worked on at least once.  Choose the
    # date of the oldest task as our starting point.

    start_time = None
    for task in tasks:
        if start_time == None or start_time > task['latest_activity']:
            start_time = task['latest_activity']

    end_time = utils.current_datetime()

    # If the selected start time is less than one hour ago, extend it out to
    # the last hour to give a more representative sample.

    if end_time - start_time < datetime.timedelta(hours=1):
        start_time = end_time - datetime.timedelta(hours=1)

    # Calculate the amount of time spent on each of these activities since
    # the oldest task.

    for task in tasks:
        task['time_spent'] = activities.time_spent_on_task(task['task'],
                                                           start_time,
                                                           end_time)

    # Calculate the total amount of time spent on all tasks thus far.

    tot_time_spent = 0
    for task in tasks:
        tot_time_spent = tot_time_spent + task['time_spent']

    # Calculate the relative amount of time spent on each task, and store this
    # as a number in the range 0..1.

    for task in tasks:
        task['relative_time_spent'] = \
                float(task['time_spent']) / float(tot_time_spent)

    # Given the desired weightings of each task, calculate the desired relative
    # time spent.

    tot_weighting = 0.00
    for task in tasks:
        tot_weighting = tot_weighting + task['task'].weighting

    if tot_weighting == 0:
        # We can't decide -> return the first task (if any).
        if len(tasks) > 0:
            return tasks[0]['task']
        else:
            return None

    for task in tasks:
        task['desired_relative_time_spent'] = \
                task['task'].weighting / tot_weighting

    # Calculate the discrepency between the desired time spent and the actual
    # time spent.

    for task in tasks:
        task['discrepency'] = task['desired_relative_time_spent'] \
                            - task['relative_time_spent']

    # Finally, choose the task with the biggest (positive) discrepency.

    biggest_task        = None
    biggest_discrepency = 0.00

    for task in tasks:
        discrepency = task['discrepency']
        if biggest_task == None or discrepency > biggest_discrepency:
            biggest_discrepency = discrepency
            biggest_task        = task['task']

    # Testing:

    print
    print "Choosing a task:"
    print
    for task in tasks:
        print "  " + task['task'].label + ":"
        print "    time_spent = ", task['time_spent']
        print "    relative_time_spent = ", task['relative_time_spent']
        print "    desired_relative_time_spent = ", \
                            task['desired_relative_time_spent']
        print "    discrepency = ", task['discrepency']
        print

    # Return the task back to the caller.

    return biggest_task

