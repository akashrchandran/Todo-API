from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Todo
from .serializers import (serialize_add_task, serialize_delete_task,
                          serialize_login, serialize_register,
                          serialize_toggle_task, serialize_update_task)


@api_view(['POST'])
def login(request):
    """
    API Description:
    This API allows users to authenticate and obtain a JWT token for accessing protected resources.

    Parameters:
    - `username` (string): The username of the user.
    - `password` (string): The password of the user.

    Response:
    - HTTP 200 OK: The request was successful. Returns a JWT token and username.
    - HTTP 401 Unauthorized: The provided credentials are invalid.
    - HTTP 400 Bad Request: The request data is invalid.
    """
    serializer = serialize_login(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username  # Add custom claim for username
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username  # Add custom claim for username
        }
        return Response(token, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def register(request):
    """
    API Description:
    This API allows users to register a new account.

    Parameters:
    - `username` (string): The desired username for the new account.
    - `first_name` (string, optional): The first name of the user.
    - `last_name` (string, optional): The last name of the user.
    - `password` (string): The password for the new account.

    Response:
    - HTTP 201 Created: The user account was created successfully. Returns a success message.
    - HTTP 400 Bad Request: The request data is invalid or the username is already taken. Returns detailed error information.
    """
    serializer = serialize_register(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get("username")
        first_name = serializer.validated_data.get("first_name") or ''
        last_name = serializer.validated_data.get("last_name") or ''
        password = serializer.validated_data["password"]

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError as e:
            print(e)
            return Response({'error': 'Username already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User created successfully, please login.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task(request):
    """
    API Description:
    This API allows authenticated users to add a new task.

    Required Permissions:
    - The user must be authenticated.

    Parameters:
    - `task` (string): The task description.
    - `date` (string): The expected date of the task completetion in format of YYYY-MM-DD.

    Response:
    - HTTP 201 Created: The task was created successfully. Returns a success message and the task ID.
    - HTTP 400 Bad Request: The request data is invalid. Returns detailed error information.
    """
    serializer = serialize_add_task(data=request.data)
    if serializer.is_valid():
        username = request.user.username
        task = serializer.validated_data.get("task")
        date = serializer.validated_data.get("date")
        # Attempt to create new user
        todo = Todo.objects.create(username=username, task=task, date=date)
        todo.save()
        return Response({'message': 'Task successfully created.', 'task_id': todo.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    """
    API Description:
    This API allows authenticated users to retrieve all their tasks.

    Required Permissions:
    - The user must be authenticated.

    Response:
    - HTTP 200 OK: The request was successful. Returns all tasks associated with the authenticated user.
    """
    username = request.user.username
    tasks = Todo.objects.filter(username=username)
    return Response(tasks.values(), status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request):
    """
    API Description:
    This API allows authenticated users to update a task.

    Required Permissions:
    - The user must be authenticated.

    Parameters:
    - `taskId` (integer): The ID of the task to be updated.
    - `updatedTask` (string): The updated task description.
    - `updatedDate` (string): The updated date of the task.
    - `completed` (boolean, optional): Indicates whether the task is completed.

    Response:
    - HTTP 200 OK: The task was updated successfully. Returns a success message.
    - HTTP 400 Bad Request: The request data is invalid or the specified task does not exist. Returns detailed error information.
    """
    serializer = serialize_update_task(data=request.data)
    if serializer.is_valid():
        username = request.user.username
        task_id = serializer.validated_data.get("taskId")
        updatedTask = serializer.validated_data.get("updatedTask")
        updatedDate = serializer.validated_data.get("updatedDate")
        # Attempt to create new user
        try:
            todo = Todo.objects.get(username=username, id=task_id)
            todo.task = updatedTask
            todo.date = updatedDate
            todo.save()
        except Todo.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Task successfully updated.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_complete(request):
    """
    API Description:
    This API allows authenticated users to toggle a task's completed status.

    Required Permissions:
    - The user must be authenticated.

    Parameters:
    - `taskId` (integer): The ID of the task to toggle its completed status.

    Response:
    - HTTP 200 OK: The task's completed status was toggled successfully. Returns a success message.
    - HTTP 400 Bad Request: The request data is invalid or the specified task does not exist. Returns detailed error information.
    """
    serializer = serialize_toggle_task(data=request.data)
    if serializer.is_valid():
        username = request.user.username
        task_id = serializer.validated_data.get("taskId")
        # Attempt to create new user
        try:
            todo = Todo.objects.get(username=username, id=task_id)
            todo.completed = not todo.completed
            todo.save()
        except Todo.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Task successfully updated.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request):
    """
    API Description:
    This API allows authenticated users to delete a task.

    Required Permissions:
    - The user must be authenticated.

    Parameters:
    - `taskId` (integer): The ID of the task to be deleted.

    Response:
    - HTTP 200 OK: The task was deleted successfully. Returns a success message.
    - HTTP 400 Bad Request: The request data is invalid or the specified task does not exist. Returns detailed error information.
    """
    serializer = serialize_delete_task(data=request.data)
    if serializer.is_valid():
        username = request.user.username
        task_id = serializer.validated_data.get("taskId")
        # Attempt to create new user
        try:
            todo = Todo.objects.get(username=username, id=task_id)
            todo.delete()
        except Todo.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Task successfully deleted.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    return HttpResponse('''<h1>Todo API</h1>
    <h2>Vist below routes for API documentation</h2>
    <ul>
    <li><a href="/api/login">/api/login</a></li>
    <li><a href="/api/register">/api/register</a></li>
    <li><a href="/api/add">/api/add</a></li>
    <li><a href="/api/get">/api/get</a></li>
    <li><a href="/api/update">/api/update</a></li>
    <li><a href="/api/complete">/api/complete</a></li>
    <li><a href="/api/delete">/api/delete</a></li>
    </ul>
    <h2>Visit <a href="https://github.com/akashrchandran/Todo-API">github repository</a> for more info</h2>
    ''')