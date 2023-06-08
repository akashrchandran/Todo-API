from rest_framework import serializers

from .models import Todo


class serialize_login(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class serialize_register(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

class serialize_add_task(serializers.Serializer):
    task = serializers.CharField(required=True)
    date = serializers.DateField(required=True, format="%Y-%m-%d")

class serialize_update_task(serializers.Serializer):
    taskId = serializers.IntegerField(required=True)
    updatedTask = serializers.CharField(required=True)
    updatedDate = serializers.DateField(required=True, format="%Y-%m-%d")

class serialize_toggle_task(serializers.Serializer):
    taskId = serializers.IntegerField(required=True)

class serialize_delete_task(serializers.Serializer):
    taskId = serializers.IntegerField(required=True)