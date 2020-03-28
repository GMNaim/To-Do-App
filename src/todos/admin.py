from django.contrib import admin
from .models import TaskList


class TaskListAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'is_completed')
    list_editable = ('is_completed',)


admin.site.register(TaskList, TaskListAdmin)