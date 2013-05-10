""" dayshaper.shared.lib.chooser

    This module implements the "task chooser" for the Dayshaper system.  This
    is responsible for choosing the next task to work on.
"""
import datetime

from dayshaper.shared.models import *
from dayshaper.shared.lib    import activities, preferences, utils

from dayshaper.shared import task_choosers

#############################################################################

def choose_next_task():
    """ Calculate the next task to work on.

        Starting at the top of the tree, we choose the top-level task to work
        on, based on the default strategy stored in our preferences. If the
        selected task has children, we then repeat the process for the child
        task, using the selected task's strategy, continuing until we reach a
        task with no children, which is the task to work on next.

        Upon completion, we return the Task object to work on next, or None if
        there are no task objects that we can work on.
    """
    parent   = None
    strategy = preferences.get_int("TOP_LEVEL_STRATEGY",
                                   Task.STRATEGY_PROPORTIONAL)

    while True:
        task = _calc_next_task_for_parent(parent, strategy)
        if task == None:
            return None

        if task.children.filter(status=Task.STATUS_ACTIVE).exists():
            # This task has at least one active child -> choose the task from
            # among this task's children.
            parent   = task
            strategy = task.strategy
            continue
        else:
            # We've reached a leaf node task -> this is the one to work on.
            return task

#############################################################################
#                                                                           #
#                    P R I V A T E   D E F I N I T I O N S                  #
#                                                                           #
#############################################################################

def _calc_next_task_for_parent(parent, strategy):
    """ Choose the next task to perform from among the given task's children.

        The parameters are as follows:

            'parent'

                The parent task to use, or None if we are choosing from among
                the top-level tasks.

            'strategy'

                The strategy to use for calculating the next task.  This will
                be an integer matching one of the STRATEGY_XXX constants
                defined within the dayshaper.shared.models.Task object.

        If there are no active child tasks for the given parent, we return
        None.
    """
    if strategy == Task.STRATEGY_PROPORTIONAL:
        return task_choosers.proportional.choose_next_task(parent)
    elif strategy == Task.STRATEGY_ROUND_ROBIN:
        return task_choosers.round_robin.choose_next_task(parent)
    elif strategy == Task.STRATEGY_FIRST_UNFINISHED:
        return task_choosers.first_unfinished.choose_next_task(parent)
    elif strategy == Task.STRATEGY_RANDOM:
        return task_choosers.random.choose_next_task(parent)
    else:
        return None

#############################################################################

def _has_children(task):
    """ Return True if this task has one or more active child tasks.
    """
    if task.children.filter(status=Task.STATUS_ACTIVE).exists():
        return True
    else:
        return False

