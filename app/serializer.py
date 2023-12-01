from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Task, TaskSummary
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
        )

    def create(self, validated_data):
        # Hash the password before saving it to the database
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserSerializer, self).create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("assigned_users",)

    def create(self, validated_data):
        user_id = self.context["request"].user.id
        user = User.objects.get(id=user_id)

        # Create the task instance without assigning users
        instance = Task.objects.create(**validated_data)

        # Assign the user to the many-to-many field
        instance.assigned_users.set([user])

        return instance


class TaskSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSummary
        fields = "__all__"

class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
