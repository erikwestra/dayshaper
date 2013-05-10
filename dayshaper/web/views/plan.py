""" dayshaper.web.views.plan

    This module implements the various views for the Dayshaper system's
    planning mode.
"""
import traceback

import simplejson as json

from django.http                  import HttpResponse, HttpResponseRedirect
from django.shortcuts             import render
from django.core.urlresolvers     import reverse
from django.views.decorators.csrf import csrf_exempt

import simplejson as json

from dayshaper.shared.models import *

#############################################################################

def plan(request):
    """ Respond to the main "/plan" URL.

        We display a the main "plan" view for the Dayshaper system.

        Note that this view makes heavy use of various AJAX event handlers,
        which are defined below.
    """
    return render(request, "plan.html",
                  {'status_choices'   : Task.STATUS_CHOICES,
                   'strategy_choices' : Task.STRATEGY_CHOICES})

#############################################################################

@csrf_exempt
def list(request):
    """ Return a list of the tasks to display in our tree view.

        This AJAX event handler takes no parameters, and returns a JSON-format
        "tree" of tasks to be displayed.

        Upon completion, we return a list of "tree nodes", where each node in
        the tree will be represented by a dictionary with the following
        entries:

            'title'

                The label to use for this task.

            'icon'

                Set to False.  This forces the "Dynatree" library to hide the
                icon for this tree node.

            'addClass'

                A CSS class name to add to the task's <span> tag.

            'isFolder'

                True if and only if this node has children.

            'children'

                A list of the child nodes for this node in the tree.  Each
                entry in this list will itself be a tree node dictionary.
    """
    try:
        def process_children(parent):
            """ Recursively walk the tree, building our tree of nodes.

                We return a list of dynatree node entries for this level of the
                tree.  Each node will have children as required to flesh out
                the entire tree.
            """
            query = Task.objects.filter(parent=parent).order_by("ordinal_rank")

            tasks = []
            for task in query:
                tasks.append(task)

            nodes = []
            for task in tasks:
                node = {}
                node['key']   = str(task.id)
                node['title'] = task.label
                node['icon']  = False

                if task.status == Task.STATUS_ACTIVE:
                    node['addClass'] = "active"
                elif task.status == Task.STATUS_DISABLED:
                    node['addClass'] = "disabled"
                elif task.status == Task.STATUS_FINISHED:
                    node['addClass']= "finished"

                if task.children.exists():
                    node['isFolder'] = True
                    node['children'] = process_children(task)
                nodes.append(node)

            return nodes

        task_tree = process_children(parent=None)
        return HttpResponse(json.dumps(task_tree), mimetype="application/json")
    except:
        traceback.print_exc()
        return HttpResponse(json.dumps([]), mimetype="application/json")

#############################################################################

@csrf_exempt
def load(request):
    """ Return the details of a task for editing.

        This AJAX event handler requires a single parameter, 'task_id',
        containing the record ID of the task to edit.

        Upon completion, we return a JSON object with the following fields:

            label
            description
            status
            weighting
            min_time
            max_time
            strategy
    """
    try:
        if request.method == "GET":
            task_id = request.GET['task_id']
        elif request.method == "POST":
            task_id = request.POST['task_id']

        task = Task.objects.get(id=task_id)
        
        response = {}
        response['label'] = task.label
        response['description'] = task.description
        response['status']      = task.status
        response['weighting']   = task.weighting
        response['min_time']    = task.min_time
        response['max_time']    = task.max_time
        response['strategy']    = task.strategy
        
        return HttpResponse(json.dumps(response), mimetype="application/json")
    except:
        traceback.print_exc()
        return HttpResponse(json.dumps({}), mimetype="application/json")

#############################################################################

@csrf_exempt
def save(request):
    """ Attempt to save the details of a task to disk.

        This AJAX event handler requires the following parameters:

            'task_id'

                The ID of the task we are editing.

            'label'
            'description'
            'status'
            'weighting'
            'min_time'
            'max_time'
            'strategy'

                The fields of the task we're trying to save.

        We attempt to save the given task's details to disk.  Upon completion,
        we return a JSON object with the following fields:

            'success'

                Set to True if and only if the task's details were saved.

            'err_msg'

                A string to dispay as an error message if the task's details
                could not be saved.
    """
    try:
        if request.method == "GET":
            params = request.GET
        elif request.method == "POST":
            params = request.POST
        else:
            params = {}

        task = Task.objects.get(id=params['task_id'])

        label       = params['label']
        description = params['description']
        status      = params['status']
        weighting   = params['weighting']
        min_time    = params['min_time']
        max_time    = params['max_time']
        strategy    = params['strategy']

        err_msg = None # initially.

        if label == "":
            err_msg = "Please enter a label for this task."
        else:
            try:
                existing_task = Task.objects.get(parent=task.parent,
                                                 label__iexact=label)
            except Task.DoesNotExist:
                existing_task = None

            if existing_task != None and task.id != existing_task.id:
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
            task.label       = label
            task.description = description
            task.status      = status
            task.weighting   = weighting
            task.min_time    = min_time
            task.max_time    = max_time
            task.strategy    = strategy

            task.save()

            return HttpResponse(json.dumps({'success' : True}),
                                mimetype="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False,
                                            'err_msg' : err_msg}),
                                mimetype="application/json")
    except:
        traceback.print_exc()
        return HttpResponse(json.dumps({'success' : False,
                                        'err_msg' : "Internal server error"}),
                            mimetype="application/json")

#############################################################################

@csrf_exempt
def add_sibling(request):
    """ Add a new sibling to a task.

        This AJAX event handler requires the following parameter:

            'task_id'

                The ID of the task to add a sibling to.

        We create a new Task object as a sibling of the given task.  The new
        Task object will be given a unique name, and placed as a sibling of the
        given task.

        Upon completion, we return a JSON object with the following fields:

            'success'

                Set to True if the new task was successfully created.

            'sibling_id'

                The record ID of the newly-created sibling task.
    """
    try:
        if request.method == "GET":
            params = request.GET
        elif request.method == "POST":
            params = request.POST
        else:
            params = {}

        existing_task = Task.objects.get(id=params['task_id'])

        # Allocate a unique label for this task.

        untitled_num = 0
        while True:
            if untitled_num == 0:
                label = "Untitled"
            else:
                label = "Untitled " + str(untitled_num)

            if Task.objects.filter(parent=existing_task.parent,
                                   label=label).exists():
                untitled_num = untitled_num + 1
                continue
            else:
                break

        # Count the number of tasks in this task's list.  We use this to assign
        # an ordinal rank to the newly-created task so that it appears at the
        # bottom of the list.

        num_tasks = Task.objects.filter(parent=existing_task.parent).count()

        # Create the new task.

        task = Task()
        task.parent       = existing_task.parent
        task.ordinal_rank = num_tasks + 1
        task.label        = label
        task.description  = ""
        task.weighting    = 1.00
        task.min_time     = 0
        task.max_time     = 0
        task.status       = Task.STATUS_ACTIVE
        task.strategy     = Task.STRATEGY_PROPORTIONAL
        task.save()

        return HttpResponse(json.dumps({'success'    : True,
                                        'sibling_id' : task.id}),
                            mimetype="application/json")
    except:
        traceback.print_exc()
        return HttpResponse(json.dumps({'success' : False}),
                            mimetype="application/json")

#############################################################################

@csrf_exempt
def add_child(request):
    """ Add a new child to a task.

        This AJAX event handler requires the following parameter:

            'task_id'

                The ID of the task to add a child to.

        We create a new Task object as a child of the given task.  The new
        Task object will be given a unique name, and placed as a child of the
        given task.

        Upon completion, we return a JSON object with the following fields:

            'success'

                Set to True if the new task was successfully created.

            'child_id'

                The record ID of the newly-created child task.
    """
    try:
        if request.method == "GET":
            params = request.GET
        elif request.method == "POST":
            params = request.POST
        else:
            params = {}

        existing_task = Task.objects.get(id=params['task_id'])

        # Allocate a unique label for this task.

        untitled_num = 0
        while True:
            if untitled_num == 0:
                label = "Untitled"
            else:
                label = "Untitled " + str(untitled_num)

            if Task.objects.filter(parent=existing_task, label=label).exists():
                untitled_num = untitled_num + 1
                continue
            else:
                break

        # Count the number of tasks in this task's list.  We use this to assign
        # an ordinal rank to the newly-created task so that it appears at the
        # bottom of the list.

        num_tasks = Task.objects.filter(parent=existing_task).count()

        # Create the new task.

        task = Task()
        task.parent       = existing_task
        task.ordinal_rank = num_tasks + 1
        task.label        = label
        task.description  = ""
        task.weighting    = 1.00
        task.min_time     = 0
        task.max_time     = 0
        task.status       = Task.STATUS_ACTIVE
        task.strategy     = Task.STRATEGY_PROPORTIONAL
        task.save()

        return HttpResponse(json.dumps({'success'  : True,
                                        'child_id' : task.id}),
                            mimetype="application/json")
    except:
        traceback.print_exc()
        return HttpResponse(json.dumps({'success' : False}),
                            mimetype="application/json")

#############################################################################

@csrf_exempt
def delete(request):
    """ Delete a task.

        This AJAX event handler requires the following parameter:

            'task_id'

                The ID of the task to delete.

        We delete the task with the given ID.

        Upon completion, we return a JSON object with the following fields:

            'success'

                Set to True if the task was successfully deleted.
    """
    try:
        if request.method == "GET":
            params = request.GET
        elif request.method == "POST":
            params = request.POST
        else:
            params = {}

        task = Task.objects.get(id=params['task_id'])
        task.delete()

        return HttpResponse(json.dumps({'success' : True}),
                            mimetype="application/json")
    except:
        traceback.print_exc()
        return HttpResponse(json.dumps({'success' : False}),
                            mimetype="application/json")

#############################################################################

@csrf_exempt
def move(request):
    """ Move a task.

        This AJAX event handler requires the following parameter:

            'src_id'

                The ID of the task to move.

            'target_id'

                The ID of the task to move this node to.

            'hit_mode'

                A string describing how to position the source node relative to
                the target node.  One of:

                    "over"
                    "before"
                    "after"

        We move the source task to the given position within the tree.  If
        'hit_mode' is "over", we make the source node a child of the target
        node; if 'hit_mode' is "before", we place the source node immediately
        before the target node; and if 'hit_mode' is 'after", we place the
        source node immediately after the target node.

        Upon completion, we return a JSON object with the following fields:

            'success'

                Set to True if the task was successfully moved.
    """
    try:
        if request.method == "GET":
            params = request.GET
        elif request.method == "POST":
            params = request.POST
        else:
            params = {}

        src_task    = Task.objects.get(id=params['src_id'])
        target_task = Task.objects.get(id=params['target_id'])
        hit_mode    = params['hit_mode']

        # Recalculate the ordinal rankings for the remaining tasks in the
        # source list.

        query = Task.objects.filter(parent=src_task.parent)

        remaining_tasks = []
        for task in query.order_by("ordinal_rank"):
            if task != src_task:
                remaining_tasks.append(task)

        ordinal_rank = 1
        for task in remaining_tasks:
            task.ordinal_rank = ordinal_rank
            task.save()
            ordinal_rank = ordinal_rank + 1

        # Calculate the parent to use for the destination list.  Note that this
        # depends on the hit mode -- if we're moving a task into a sub-list,
        # the "target" is actually the destination.  Otherwise, the target's
        # parent will be the destination.

        if hit_mode == "over":
            dest_parent = target_task
        else:
            dest_parent = target_task.parent

        # Move the source task into the destination list.

        src_task.parent = dest_parent
        src_task.save()

        # Build a list of the tasks in the destination list (excluding the
        # source task, which we'll add separately).

        query = Task.objects.filter(parent=dest_parent)

        dest_tasks = []
        for task in query.order_by("ordinal_rank"):
            if task != src_task:
                dest_tasks.append(task)

        # Insert the source task into the destination list, in the correct
        # position.

        if hit_mode == "over":
            # Simply append the task to the end of the list.
            dest_tasks.append(src_task)
        else:
            i = dest_tasks.index(target_task)
            if hit_mode == "before":
                dest_tasks.insert(i, src_task)
            else:
                dest_tasks.insert(i+1, src_task)

        # Finally, recalculate the ordinal rankings for the tasks in the
        # destination list.

        ordinal_rank = 1
        for task in dest_tasks:
            task.ordinal_rank = ordinal_rank
            task.save()
            ordinal_rank = ordinal_rank + 1

        # That's all, folks!

        return HttpResponse(json.dumps({'success' : True}),
                            mimetype="application/json")
    except:
        traceback.print_exc()
        return HttpResponse(json.dumps({'success' : False}),
                            mimetype="application/json")

