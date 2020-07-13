import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import TaskList


def home(request):
    """Rendering home page of the application"""
    task_list = TaskList.objects.all()
    context = {'task_list': task_list}
    if request.method == 'GET':
        return render(request, 'todos/home.html', context)

    return render(request, 'todos/home.html', context)


@require_POST
def add_task(request):
    """ Adding a new to-do task """
    if request.method == 'POST':
        task = request.POST['add_task']
        time_left = request.POST['input_endtime']
        hour_minutes = str(time_left).split(':')
        time_now = datetime.datetime.now()
        year = time_now.today().year
        month = time_now.today().month
        day = datetime.datetime.today().day
        hour = int(hour_minutes[0])
        minutes = int(hour_minutes[1])
        
        time_left_after_calculation = time_now.replace(
            year=year, month=month, day=day, hour=hour, minute=minutes)
        task_list = TaskList.objects.create(
            task=task, time_left=time_left_after_calculation)
        task_list.save()

    return redirect('home')


def completed_task(request):
    """ Completing the task if user check the task """
    task_list = TaskList.objects.all()
    context = {'task_list': task_list}
    if request.POST:
        task_is_checked = request.POST.get('task_is_checked')
        task_checked_id = request.POST.get('task_checked_id')
        
        get_task = TaskList.objects.get(pk=task_checked_id)
        
        if task_is_checked:
            get_task.is_completed = True
            get_task.save()

        if request.is_ajax():
            return JsonResponse({'task_is_checked': task_is_checked,
                                 'task_checked_id': task_checked_id,
                                 'checked_view_text': "From View Checked:"}, status=200)

    return render(request, 'todos/home.html', context)


def uncompleted_task(request):
    """ Make the completed task incomplete if use uncheck the task."""
    task_list = TaskList.objects.all()
    context = {'task_list': task_list}
    if request.POST:
        task_is_unchecked = request.POST['task_is_unchecked']
        task_unchecked_id = request.POST['task_unchecked_id']
        get_task = TaskList.objects.get(pk=task_unchecked_id)
        if task_is_unchecked:
            get_task.is_completed = False
            get_task.save()
            
        if request.is_ajax():
            return JsonResponse({'task_is_unchecked': task_is_unchecked,
                                 'task_unchecked_id': task_unchecked_id,
                                 'unchecked_view_text': "From View UnChecked:"}, status=200)

    return render(request, 'todos/home.html', context)


def edit_task(request, task_id):
    """ Editing the created task """
    if request.POST:
        edit_task_id = request.POST['edited_task_id']
        edited_task = request.POST['edited_task']
        get_task = TaskList.objects.get(pk=edit_task_id)
        get_task.task = edited_task
        get_task.save()

        return JsonResponse({'edited_task_from_view': get_task.task, 'edited_task_id_from_view': edit_task_id}, status=200)

    return render(request, 'todos/home.html')


def delete_task(request, task_id):
    """ Deleting the task """
    task_list = TaskList.objects.all()
    context = {'task_list': task_list}

    if request.POST:
        deleted_task_id = request.POST.get('deleted_task_id')
        get_task = TaskList.objects.get(pk=task_id)
        get_task.delete()
        return JsonResponse({'deleted_task_id_from_view': deleted_task_id, 'deleted_text': "task deleted"}, status=200)

    return render(request, 'todos/home.html', context)
