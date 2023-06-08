from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('add/', views.add_task, name='Add new Task'),
    path('get/', views.get_tasks, name='Get all Tasks'),
    path('update/', views.update_task, name='Update Task'),
    path('complete/', views.toggle_complete, name='Toggle Complete of Task'),
    path('delete/', views.delete_task, name='Delete Task'),
]