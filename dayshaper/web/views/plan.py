""" dayshaper.web.views.plan

    This module implements the various views for the Dayshaper system's
    planning mode.
"""
from django.http      import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from dayshaper.shared.models import *

#############################################################################

def list(request, parent_id=None):
    """ Respond to the main "/plan" URL.

        'parent_id' is the record ID of the current parent to use for
        viewing/editing the list of tasks, if any.

        We display a list of the various tasks with the given parent, with
        options to add/edit/delete tasks, and to drill down or more up the
        hierarchy of tasks.
    """
    # Start by calculating the heading to use for this page.  This is based on
    # the path up from the current parent ID.

    if parent_id == None:
        heading = "Top-Level Tasks:"
    else:
        parent_path = []
        a_parent_id = parent_id
        while a_parent_id != None:
            parent = Task.objects.get(id=a_parent_id)
            parent_path.append(parent.label)
            a_parent_id = parent.parent_id
        heading = "&nbsp;/&nbsp;".join(reversed(parent_path)) + " Tasks:"

    # Calculate the list of tasks at this level.

    query = Task.objects.filter(parent=parent_id)
    query = query.extra(select={'lower_label' : "lower(shared_task.label)"})
    query = query.order_by("lower_label")

    tasks = []
    for task in query:
        t = {}
        t['id']           = task.id
        t['has_children'] = (task.children.exists())
        t['label']        = task.label
        t['weighting']    = task.weighting
        tasks.append(t)

    # Calculate the various URLs we'll need for this page.

    edit_url     = "/plan/edit"
    children_url = "/plan"
    delete_url   = "/plan/delete"

    if parent_id == None:
        add_url = "/plan/add"
    else:
        add_url = "/plan/add/" + str(parent_id)

    if parent_id != None:
        parent = Task.objects.get(id=parent_id)
        if parent.parent != None:
            up_url = "/plan/" + str(parent.parent_id)
        else:
            up_url = "/plan/"
    else:
        up_url = None

    done_url = "/"

    # Finally, display the page.

    return render(request, "plan.html",
                  {'heading'      : heading,
                   'tasks'        : tasks,
                   'edit_url'     : edit_url,
                   'children_url' : children_url,
                   'delete_url'   : delete_url,
                   'add_url'      : add_url,
                   'up_url'       : up_url,
                   'done_url'     : done_url})

#############################################################################

def add(request, parent_id=None):
    """ Respond to the "/plan/add" URL.

        'parent_id' is the record ID of the parent to use for the newly-added
        task, if any.

        We let the user add a new task.
    """
    if request.method == "GET":

        # We're displaying the form for the first time.  Set our defaults.

        label       = ""
        description = ""
        weighting   = "1.0"
        min_time    = "0"
        max_time    = "0"
        err_msg     = None

    elif request.method == "POST":

        # Respond to the user submitting our form.

        if request.POST.get("cancel") == "Cancel":
            if parent_id == None:
                return HttpResponseRedirect("/plan")
            else:
                return HttpResponseRedirect("/plan/" + str(parent_id))

        label       = request.POST['label']
        description = request.POST['description']
        weighting   = request.POST['weighting']
        min_time    = request.POST['min_time']
        max_time    = request.POST['max_time']

        err_msg = None # initially.

        if label == "":
            err_msg = "Please enter a label for this task."
        else:
            try:
                existing_task = Task.objects.get(parent=parent_id,
                                                 label__iexact=label)
            except Task.DoesNotExist:
                existing_task = None

            if existing_task != None:
                err_msg = "There is already a task with that label."

        if err_msg == None:
            try:
                weighting = float(weighting)
            except ValueError:
                err_msg = "Weighting must be a number."

        if err_msg == None:
            if weighting < 0:
                err_msg = "Weighting can't be negative."

        if err_msg == None:
            try:
                min_time = int(min_time)
            except ValueError:
                err_msg = "Minimum time must be a number."

        if err_msg == None:
            if min_time < 0:
                err_msg = "Minimum time can't be negative."

        if err_msg == None:
            try:
                max_time = int(max_time)
            except ValueError:
                err_msg = "Maximum time must be a number."

        if err_msg == None:
            if min_time < 0:
                err_msg = "Maximum time can't be negative."
            elif max_time < min_time:
                err_msg = "Maximum time can't be lower than minimum."

        if err_msg == None:

            # The entered values are acceptable -> create the new task.

            task = Task()

            if parent_id != None:
                task.parent = Task.objects.get(id=parent_id)
            else:
                task.parent = None

            task.label       = label
            task.description = description
            task.weighting   = weighting
            task.min_time    = min_time
            task.max_time    = max_time
            task.delay_until = None
            task.save()

            # Return back to the "plan" view for the parent task.

            if parent_id == None:
                return HttpResponseRedirect("/plan")
            else:
                return HttpResponseRedirect("/plan/" + str(parent_id))

    # If we get here, we're either displaying the form for the first time, or
    # there was an error.  Either way, display the page to the user.

    if parent_id == None:
        heading = "Add Top-Level Task"
    else:
        parent  = Task.objects.get(id=parent_id)
        heading = "Add " + parent.label + " Task"

    return render(request, "edit.html",
                  {'heading'     : heading,
                   'label'       : label,
                   'description' : description,
                   'weighting'   : weighting,
                   'min_time'    : min_time,
                   'max_time'    : max_time,
                   'err_msg'     : err_msg})

#############################################################################

def edit(request, task_id):
    """ Respond to the "/plan/edit/X" URL.

        'task_id' is the ID of the task to edit.

        We let the user edit the details of the given task.
    """
    task = Task.objects.get(id=task_id)

    if request.method == "GET":

        # We're displaying the form for the first time.  Set up our initial
        # values.

        label       = task.label
        description = task.description
        weighting   = str(task.weighting)
        min_time    = str(task.min_time)
        max_time    = str(task.max_time)
        err_msg     = None

    elif request.method == "POST":

        # Respond to the user submitting our form.

        if request.POST.get("cancel") == "Cancel":
            if task.parent == None:
                return HttpResponseRedirect("/plan")
            else:
                return HttpResponseRedirect("/plan/" + str(task.parent.id))

        label       = request.POST['label']
        description = request.POST['description']
        weighting   = request.POST['weighting']
        min_time    = request.POST['min_time']
        max_time    = request.POST['max_time']

        err_msg = None # initially.

        if label == "":
            err_msg = "Please enter a label for this task."
        else:
            try:
                existing_task = Task.objects.get(parent=task.parent,
                                                 label__iexact=label)
            except Task.DoesNotExist:
                existing_task = None

            if existing_task != None and existing_task != task:
                err_msg = "That label is used by another task."

        if err_msg == None:
            try:
                weighting = float(weighting)
            except ValueError:
                err_msg = "Weighting must be a number."

        if err_msg == None:
            if weighting < 0:
                err_msg = "Weighting can't be negative."

        if err_msg == None:
            try:
                min_time = int(min_time)
            except ValueError:
                err_msg = "Minimum time must be a number."

        if err_msg == None:
            if min_time < 0:
                err_msg = "Minimum time can't be negative."

        if err_msg == None:
            try:
                max_time = int(max_time)
            except ValueError:
                err_msg = "Maximum time must be a number."

        if err_msg == None:
            if min_time < 0:
                err_msg = "Maximum time can't be negative."
            elif max_time < min_time:
                err_msg = "Maximum time can't be lower than minimum."

        if err_msg == None:

            # The entered values are acceptable -> update the task.

            task.label       = label
            task.description = description
            task.weighting   = weighting
            task.min_time    = min_time
            task.max_time    = max_time
            task.save()

            # Return back to the "plan" view for the parent task.

            if task.parent == None:
                return HttpResponseRedirect("/plan")
            else:
                return HttpResponseRedirect("/plan/" + str(task.parent.id))

    # If we get here, we're either displaying the form for the first time, or
    # there was an error.  Either way, display the page to the user.

    if task.parent == None:
        heading = "Edit Top-Level Task"
    else:
        heading = "Edit " + task.parent.label + " Task"

    return render(request, "edit.html",
                  {'heading'     : heading,
                   'label'       : label,
                   'description' : description,
                   'weighting'   : weighting,
                   'min_time'    : min_time,
                   'max_time'    : max_time,
                   'err_msg'     : err_msg})

#############################################################################

def delete(request, task_id):
    """ Respond to the "/plan/delete/X" URL.

        We let the user delete the given task.
    """
    task = Task.objects.get(id=task_id)

    if request.method == "POST":

        # The user is submitting our form.  If they confirmed the deletion, go
        # ahead and delete this task.

        if request.POST['confirm'] == "1":
            task.delete()

        # Either way, return back to the main "plan" view.

        if task.parent == None:
            return HttpResponseRedirect("/plan")
        else:
            return HttpResponseRedirect("/plan/" + str(task.parent.id))

    # If we get here, we're displaying the page for the first time.  Display
    # the "confirmation" page.

    return render(request, "confirm.html",
                  {'title'   : "Dayshaper",
                   'heading' : "Delete Task",
                   'message' : "Are you sure you want to delete the &ldquo;" +
                               task.label + "&rdquo; task?"})

