""" dayshaper.shared.task_choosers.round_robin

    This module implements the "round robin" task chooser for the Dayshaper
    system.  This chooses the next task so that tasks are worked on in a
    round-robin fashion.
"""
from dayshaper.shared.models import *
from dayshaper.shared.lib    import activities, utils

#############################################################################

def choose_next_task(parent):
    """ Choose the next task to work on from among the given task's children.

        Upon completion, we return the Task object to work on next, or None if
        there are no active task objects.
    """
    # Build a list of the active tasks which have the given parent.

    query = Task.objects.filter(parent=parent, status=Task.STATUS_ACTIVE)

    tasks = []
    for task in query.order_by("ordinal_rank"):
        tasks.append({'task' : task})

    if len(tasks) == 0:
        # There are no tasks we can work on -> give up.
        return None

    # Calculate the latest activity for each task.

    for task in tasks:
        task['latest_activity'] = \
            activities.latest_activity_for_task(task['task'])

    # If a task has never been worked on, work on it now.

    for task in tasks:
        if task['latest_activity'] == None:
            return task

    # If we get here, we've worked on every task at some stage.  In this case,
    # we find the most-recently worked-on task, and choose the one immediately
    # after it.

    latest_index = None
    latest_time  = None

    for i,task in enumerate(tasks):
        if (latest_time == None) or (task['latest_activity'] > latest_time):
            latest_index = i
            latest_time  = task['latest_activity']

    if latest_index == len(tasks)-1:
        return tasks[0]['task']
    else:
        return tasks[latest_index+1]['task']

