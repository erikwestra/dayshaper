""" dayshaper.shared.lib.activities

    This module provides various utility functions for working with Activity
    objects.
"""
import operator

from dayshaper.shared.models import *

#############################################################################

def record_activity(task, start_time, end_time):
    """ Record the fact that the user worked on the given activity.

        The parameters are as follows:

            'task'

                The Task object that this activity is for.

            'start_time'

                A datetime.datetime object representing the date and time at
                which this activity was started.

            'end_time'

                A datetime.datetime object representing the date and time at
                which this activity was ended.

        Note that we insert Activity records for this activity, not only for
        this task but all parent tasks above it.
    """
    while task != None:
        activity = Activity()
        activity.task = task
        activity.started_at = start_time
        activity.ended_at   = end_time
        activity.save()

        task = task.parent

#############################################################################

def time_spent_on_task(task, start_time, end_time):
    """ Calculate how much time was spent on the given task.

        The parameters are as follows:

            'task'

                The Task object to get recent activity for.

            'start_time'

                A datetime.datetime object representing the start of the
                desired time period.

            'end_time'

                A datetime.datetime object representing the end of the desired
                time period.

        We calculate the total amount of time spent on the given task in the
        given time period.  Upon completion, we return an integer number of
        seconds representing the total amount of time spent on the given task
        in the given period.
    """
    total_time = 0
    for activity in Activity.objects.filter(task=task,
                                            started_at__lte=end_time,
                                            ended_at__gte=start_time):
        activity_start_time = max(start_time, activity.started_at)
        activity_end_time   = min(end_time,   activity.ended_at)
        time_spent          = activity_end_time - activity_start_time
        total_time          = total_time + int(time_spent.total_seconds())

    return total_time

#############################################################################

def tasks_worked_on(start_time, end_time):
    """ Return a list of the tasks worked on in the given time period.

        The parameters are as follows:

            'start_time'

                A datetime.datetime object representing the start of the
                desired time period.

            'end_time'

                A datetime.datetime object representing the end of the desired
                time period.

        We return a list of all the tasks which have been worked on in the
        given time period.
    """
    tasks = []
    for activity in Activity.objects.filter(started_at__lte=end_time,
                                            ended_at__gte=start_time):
        tasks.append(activity.task)
    return tasks

#############################################################################

def latest_activity_for_task(task):
    """ Return the date and time at which we last worked on the given task.

        If the task has never been worked on, we return None.
    """
    latest = None
    for activity in Activity.objects.filter(task=task):
        if latest == None or latest < activity.started_at:
            latest = activity.started_at
    return latest

#############################################################################

def calc_task_summary(start_time, end_time):
    """ Calculate and return a summary of activity over a given time period.

        The parameters are as follows:

            'start_time'

                A datetime.datetime object representing the start of the
                desired time period.

            'end_time'

                A datetime.datetime object representing the end of the desired
                time period.

        We return a dictionary containing the calculated summary.  This
        dictionary will have the following entries:

            'summary'

                A "tree" of tasks worked on over the given time period, in the
                form of a list of "activity nodes".  For each "activity node",
                the list item will be a dictionary with the following entries:

                    'task'

                        The Task object.

                    'time_spent'

                        The amount of time spent on this task, in seconds.

                    'children'

                        A list of activity nodes for this task's children.  If
                        this task has no children, or there was no activity for
                        this task's children, this list will be empty.

                At each level of the tree, the tasks are sorted in reverse
                order of 'time_spent' -- that is, the task that was worked on
                the most will appear at the top.

            'tot_time'

                The total amount of time spent on all tasks during the
                day, in seconds.  Note that this only includes "leaf" nodes of
                the tree, to avoid double-counting activities for higher-level
                nodes.
    """
    summary_tree = []
    task_refs    = {} # Maps each task's record ID to the activity node in the
                      # summary tree for that task.

    for task in tasks_worked_on(start_time, end_time):

        # Build a list of the task's ancestors.  We'll have to add these to the
        # tree from the highest-level ancestor down.

        ancestors = []
        parent = task.parent
        while parent != None:
            ancestors.append(parent)
            parent = parent.parent

        # Add the ancestors, going from the highest level to the lowest level,
        # to the summary tree.

        for ancestor in reversed(ancestors):
            if ancestor.id not in task_refs:
                # This is the first time we've encountered this ancestor.  Add
                # it to the tree.
                activity_node = {'task'       : ancestor,
                                 'time_spent' : time_spent_on_task(ancestor,
                                                                   start_time,
                                                                   end_time),
                                 'children'   : []}
                if ancestor.parent == None:
                    summary_tree.append(activity_node)
                else:
                    parent_ref = task_refs[ancestor.parent.id] # Will exist.
                    parent_ref['children'].append(activity_node)

                task_refs[ancestor.id] = activity_node

        # Finally, add this task to the summary tree, if we haven't already
        # added it.

        if task.id not in task_refs:
            activity_node = {'task'       : task,
                             'time_spent' : time_spent_on_task(task,
                                                               start_time,
                                                               end_time),
                             'children'   : []}
            
            if task.parent == None:
                summary_tree.append(activity_node)
            else:
                parent_ref = task_refs[task.parent.id] # Guaranteed to exist.
                parent_ref['children'].append(activity_node)

            task_refs[task.id] = activity_node

    # Sort the summary tree by each task's "time_spent" value.

    def _sort(tree):
        """ Recursively sort the tree.
        """
        tree.sort(key=operator.itemgetter("time_spent"),
                  reverse=True)
        for node in tree:
            _sort(node['children'])

    _sort(summary_tree)

    # Calculate the total amount of time spent on the "leaf nodes" of the tree.

    def _calc_time(tree):
        """ Recursively calculate the total amount of time spent on leaf nodes.
        """
        tot_time = 0
        for node in tree:
            if len(node['children']) == 0:
                tot_time = tot_time + node['time_spent']
            else:
                tot_time = tot_time + _calc_time(node['children'])
        return tot_time

    tot_time = _calc_time(summary_tree)

    # That's all, folks!

    return {'summary'  : summary_tree,
            'tot_time' : tot_time}

#############################################################################

def latest_activity():
    """ Return the latest activity done by the user.

        We return a dictionary with the following entries:

            'task'

                The Task object most recently worked on, or None if no tasks
                have been worked on.

            'ended_at'

                A datetime.datetime object representing the date and time at
                which the user finished working on this task.

            'time_spent'

                The amount of time the user spent working on this task, in
                seconds.
    """
    try:
        activity = Activity.objects.latest("ended_at")
    except Activity.DoesNotExist:
        return {'task'       : None,
                'ended_at'   : None,
                'time_spent' : 0}

    time_spent = activity.ended_at - activity.started_at
    return {'task'       : activity.task,
            'ended_at'   : activity.ended_at,
            'time_spent' : int(time_spent.total_seconds())}

