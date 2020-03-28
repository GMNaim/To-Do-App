from django.urls import path
from .views import home, add_task, completed_task, uncompleted_task, delete_task, edit_task
urlpatterns = [
    path('', home, name='home'),
    path('add/', add_task, name='add-task'),
    path('completed/', completed_task, name='completed-task'),
    path('uncompleted/', uncompleted_task, name='uncompleted-task'),
    path('<str:task_id>/delete/', delete_task, name='delete-task'),
    path('<str:task_id>/edit/', edit_task, name='edit-task'),


]
