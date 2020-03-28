import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import TaskList


def home(request):
    task_list = TaskList.objects.all()
    context = {'task_list': task_list}
    if request.method == 'GET':
        print('=========get method===========')

        return render(request, 'todos/home.html', context)

    return render(request, 'todos/home.html', context)


@require_POST
def add_task(request):
    if request.method == 'POST':
        task = request.POST['add_task']
        time_left = request.POST['input_endtime']
        print('--------------------', task, time_left)
        hour_minutes = str(time_left).split(':')
        print('=++++++++++++++', hour_minutes)
        time_now = datetime.datetime.now()
        year = time_now.today().year
        month = time_now.today().month
        day = datetime.datetime.today().day
        print(time_now, year, month, day, '========================')
        hour = int(hour_minutes[0])
        minutes = int(hour_minutes[1])
        print(hour, minutes)

        time_left_after_calculation = time_now.replace(
            year=year, month=month, day=day, hour=hour, minute=minutes)
        task_list = TaskList.objects.create(
            task=task, time_left=time_left_after_calculation)
        print(time_left_after_calculation, "=======time_left_after_calculation")
        task_list.save()
        print(time_now)

    return redirect('home')


def completed_task(request):
    task_list = TaskList.objects.all()
    context = {'task_list': task_list}
    if request.POST:
        task_is_checked = request.POST.get('task_is_checked')
        task_checked_id = request.POST.get('task_checked_id')
        print(task_is_checked, '===================', task_checked_id)
        get_task = TaskList.objects.get(pk=task_checked_id)
        print(get_task)
        if task_is_checked:
            print(task_is_checked, 'in if block... task completed')
            get_task.is_completed = True
            get_task.save()
            print('task is true')

        if request.is_ajax():
            return JsonResponse({'task_is_checked': task_is_checked,
                                 'task_checked_id': task_checked_id,
                                 'checked_view_text': "From View Checked:"}, status=200)

    return render(request, 'todos/home.html', context)


def uncompleted_task(request):
    task_list = TaskList.objects.all()
    context = {'task_list': task_list}
    if request.POST:
        task_is_unchecked = request.POST['task_is_unchecked']
        task_unchecked_id = request.POST['task_unchecked_id']
        get_task = TaskList.objects.get(pk=task_unchecked_id)
        print(get_task)
        if task_is_unchecked:
            print("======= in if block")
            get_task.is_completed = False
            get_task.save()
            print('task is false, unchecked!====== task is uncompleted')
        if request.is_ajax():
            return JsonResponse({'task_is_unchecked': task_is_unchecked,
                                 'task_unchecked_id': task_unchecked_id,
                                 'unchecked_view_text': "From View UnChecked:"}, status=200)

    return render(request, 'todos/home.html', context)


def edit_task(request, task_id):
    if request.POST:
        edit_task_id = request.POST['edited_task_id']
        edited_task = request.POST['edited_task']
        print("edit task id=", edit_task_id)
        get_task = TaskList.objects.get(pk=edit_task_id)
        get_task.task = edited_task
        print('edited task= ', get_task.task, ' and getting task by ajax is: ', edited_task)
        get_task.save()

        return JsonResponse({'edited_task_from_view': get_task.task, 'edited_task_id_from_view': edit_task_id}, status=200)

    return render(request, 'todos/home.html')


def delete_task(request, task_id):
    task_list = TaskList.objects.all()
    context = {'task_list': task_list}

    if request.POST:
        deleted_task_id = request.POST.get('deleted_task_id')
        print(deleted_task_id, 'deleted task id......')
        get_task = TaskList.objects.get(pk=task_id)
        print(get_task, '============ task to delete')
        get_task.delete()
        return JsonResponse({'deleted_task_id_from_view': deleted_task_id, 'deleted_text': "task deleted"}, status=200)

    return render(request, 'todos/home.html', context)
