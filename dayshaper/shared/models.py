""" dayshaper.shared.models

    This module defines the core database tables for the Dayshaper system.
"""
from django.db import models

#############################################################################

class Task(models.Model):
    """ A single task within the Dayshaper system.

        Note that tasks can stand alone, or can have child tasks associated
        with them.  The "parent_task" field defines a hierarchy of tasks.
    """
    STATUS_ACTIVE   = 1
    STATUS_DISABLED = 2
    STATUS_FINISHED = 3

    STATUS_CHOICES = ([STATUS_ACTIVE,   "active"],
                      [STATUS_DISABLED, "disabled"],
                      [STATUS_FINISHED, "finished"])

    STRATEGY_PROPORTIONAL     = 1
    STRATEGY_ROUND_ROBIN      = 2
    STRATEGY_FIRST_UNFINISHED = 3
    STRATEGY_RANDOM           = 4

    STRATEGY_CHOICES = ([STRATEGY_PROPORTIONAL,     "proportional"],
                        [STRATEGY_ROUND_ROBIN,      "round robin"],
                        [STRATEGY_FIRST_UNFINISHED, "first unfinished"],
                        [STRATEGY_RANDOM,           "random"])

    id           = models.AutoField(primary_key=True)
    parent       = models.ForeignKey("Task", null=True,
                                     related_name="children")
    ordinal_rank = models.IntegerField()
    label        = models.TextField()
    description  = models.TextField()
    weighting    = models.FloatField()
    min_time     = models.IntegerField() # Time in seconds.
    max_time     = models.IntegerField() # Time in seconds.
    status       = models.IntegerField(choices=STATUS_CHOICES,
                                       default=STATUS_ACTIVE)
    strategy     = models.IntegerField(choices=STRATEGY_CHOICES,
                                       default=STRATEGY_PROPORTIONAL)

    def __unicode__(self):
        return self.label


    def get_status_label(self):
        """ Return the label to use for this task's "status" value.
        """
        for status,label in Task.STATUS_CHOICES:
            if self.status == status:
                return label
        return "???"


    def get_strategy_label(self):
        """ Return the label to use for this tasks "strategy" value.
        """
        for strategy,label in Task.STRATEGY_CHOICES:
            if self.strategy == strategy:
                return label
        return "???"

#############################################################################

class Activity(models.Model):
    """ Some work done on a task.

        We keep track of the time spent on each task, and use it to decide
        which task to work on next.
    """
    id         = models.AutoField(primary_key=True)
    task       = models.ForeignKey("Task", related_name="activities")
    started_at = models.DateTimeField(db_index=True)
    ended_at   = models.DateTimeField(db_index=True)

#############################################################################

class PreferenceSetting(models.Model):
    """ A preference setting for the application as a whole.

        Preference settings consist of name/value pairs that define preferences
        set for the application as a whole.  Note that the values are stored in
        the database as text; the shared.lib.preferences module provides
        functions to get and set the preferences using a variety of different
        types.
    """
    id    = models.AutoField(primary_key=True)
    name  = models.TextField()
    value = models.TextField()

