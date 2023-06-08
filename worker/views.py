from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.contrib.auth.models import User
from .models import Todo
from rest_framework.decorators import api_view


@api_view(['POST'])
def login(request):
    """
    - Use this endpoint to obtain JWT.
    - The JWT token will be used to authenticate other requests to the API. 
    - The token is valid for 5 minitues.
    """
    username = request.data.get('username')
    password = request.data.get('password')

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



@api_view(['POST'])
def register(request):
    """
    - Use this endpoint to register new user.
    - To register, you must provide username, password, first_name[optional], last_name[optional].
    - To get JWT token use the login endpoint.
    """
    username = request.data.get("username")
    first_name = request.data.get("first_name") or ''
    last_name = request.data.get("last_name") or ''
    password = request.data["password"]

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
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_task(request):
    print(request.user.username)
    date = request.data.get("date")
    task = request.data.get("task")
    # Attempt to create new user
    todo = Todo.objects.create(username=request.user.username, task=task, date=date)
    todo.save()
    return Response({'message': 'Task successfully created.', 'task_id': todo.id}, status=status.HTTP_201_CREATED)