""" dayshaper.shared.task_choosers.random

    This module implements the "random" task chooser for the Dayshaper system.
    This chooses a task at random.
"""
from dayshaper.shared.models import *

#############################################################################

def choose_next_task(parent):
    """ Choose the next task to work on from among the given task's children.

        Upon completion, we return the Task object to work on next, or None if
        there are no active task objects.
    """
    return None # More to come...

