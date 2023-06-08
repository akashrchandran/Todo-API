from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Todo
from .serializers import serialize_login, serialize_register, serialize_add_task, serialize_update_task, serialize_toggle_task, serialize_delete_task


@api_view(['POST'])
def login(request):
    """
    - Use this endpoint to obtain JWT.
    - The JWT token will be used to authenticate other requests to the API. 
    - The token is valid for 5 minitues.
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
    - Use this endpoint to register new user.
    - To register, you must provide username, password, first_name[optional], last_name[optional].
    - To get JWT token use the login endpoint.
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
    - Use this endpoint to add new task.
    - To add task, you must provide task, date.
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
    - Use this endpoint to get all tasks.
    """
    username = request.user.username
    tasks = Todo.objects.filter(username=username)
    return Response(tasks.values(), status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request):
    """
    - Use this endpoint to update a task.
    - To update task, you must provide task_id, task, date, completed.
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
    - Use this endpoint to toggle a task's completed status.
    - To toggle, you must provide task_id.
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
    - Use this endpoint to delete a task.
    - To delete, you must provide task_id.
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