from django.urls import path
from .views import login, register, add_task

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('addTask/', add_task, name='addTask'),
]