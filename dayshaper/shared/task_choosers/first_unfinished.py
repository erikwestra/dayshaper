""" dayshaper.shared.task_choosers.first_unfinished

    This module implements the "first unfinished" task chooser for the
    Dayshaper system.  This chooses the first unfinished task from the list of
    children.
"""
from dayshaper.shared.models import *

#############################################################################

def choose_next_task(parent):
    """ Choose the next task to work on from among the given task's children.

        Upon completion, we return the Task object to work on next, or None if
        there are no active task objects.
    """
    return None # More to come...

