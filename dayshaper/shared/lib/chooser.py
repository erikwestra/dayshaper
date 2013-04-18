""" dayshaper.shared.lib.chooser

    This module implements the "task chooser" for the Dayshaper system.  This
    is responsible for calculating the next task to work on.
"""
from dayshaper.shared.models import *
from dayshaper.shared.lib    import activities, utils

#############################################################################

def choose_next_task():
    """ Calculate the next task to work on.

        Upon completion, we return the Task object to work on next, or None if
        there are no task objects.
    """
    parent = None
    while True:
        task = _calc_next_task_for_parent(parent)
        if task.children.count() == 0:
            # We've reached a leaf node task -> this is the one to work on.
            return task
        else:
            # Choose the task from among this task's children.
            parent = task
            continue

#############################################################################
#                                                                           #
#                    P R I V A T E   D E F I N I T I O N S                  #
#                                                                           #
#############################################################################

def _calc_next_task_for_parent(parent):
    """ Choose the next task to perform from among the given task's children.

        If there are no child tasks for the given parent, we return None
    """
    # Build a list of the tasks which have the given parent.

    tasks = []
    for task in Task.objects.filter(parent=parent):
        tasks.append({'task' : task})

    # Calculate the amount of time spent on each of these activities since
    # midnight.

    start_time = utils.start_of_day()
    end_time   = utils.current_datetime()

    for task in tasks:
        task['time_spent'] = activities.time_spent_on_task(task['task'],
                                                           start_time,
                                                           end_time)

    # Calculate the total amount of time spent on all tasks thus far today.

    tot_time_spent = 0
    for task in tasks:
        tot_time_spent = tot_time_spent + task['time_spent']

    # If we haven't done any work on any of the tasks, choose the task that
    # hasn't been worked on for the longest.

    if tot_time_spent == 0:
        oldest_task = None
        oldest_date = None
        for task in tasks:
            date = activities.latest_activity(task['task'])
            is_oldest = False
            if oldest_task == None:
                is_oldest = True
            elif date == None and oldest_date != None:
                # Task never done -> it's the oldest.
                is_oldest = True
            elif date != None and oldest_date != None and date < oldest_date:
                # Both tasks have been done before, but this one was done
                # earlier -> it's the oldest.
                is_oldest = True
            if is_oldest:
                oldest_task = task['task']
                oldest_date = date
        return oldest_task

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
        print "    desired_relative_time_spent = ", task['desired_relative_time_spent']
        print "    discrepency = ", task['discrepency']
        print

    # Return the task back to the caller.

    return biggest_task
