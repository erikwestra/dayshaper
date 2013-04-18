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
    id          = models.AutoField(primary_key=True)
    parent      = models.ForeignKey("Task", null=True, related_name="children")
    label       = models.TextField()
    description = models.TextField()
    weighting   = models.FloatField()
    min_time    = models.IntegerField() # Time in seconds.
    max_time    = models.IntegerField() # Time in seconds.
    delay_until = models.DateTimeField(null=True)
    schedule    = models.TextField() # Specially formatted string.

    def __unicode__(self):
        return self.label

#############################################################################

class Activity(models.Model):
    """ Some work done on a task.

        We keep track of the time spent on each task, and use it to decide
        which task to work on next.
    """
    id         = models.AutoField(primary_key=True)
    task       = models.ForeignKey("Task", related_name="activities")
    started_at = models.DateTimeField()
    ended_at   = models.DateTimeField()

