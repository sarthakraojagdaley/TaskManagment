from __future__ import annotations

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from django.http.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Task, TaskSummary
from rest_framework.generics import CreateAPIView
from .serializer import (
    TaskSerializer,
    TaskSummarySerializer,
    UserEmailSerializer,
    UserSerializer,
    TaskDataSerializer,
)
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from app.consumers import TaskConsumer


class AddTask(CreateAPIView):
    """This view use for create the task"""

    serializer_class = TaskDataSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            task_instance = serializer.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                TaskConsumer.group_name,
                {
                    "type": "send.update",
                    "data": {
                        "title": task_instance.title,
                        "description": task_instance.description,
                    },
                },
            )
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTask(RetrieveUpdateAPIView): 
    """This view use to update the Task"""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = "pk"  # Adjust to your actual primary key field name

    def put(self, request, *args, **kwargs):
        try:
            response = super().put(request, *args, **kwargs)
        except Exception as e:
            print(f"Error updating task: {str(e)}")
            return Response(
                {"error": "Failed to update task."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {"message": "Task updated successfully.", "data": response.data},
            status=status.HTTP_200_OK,
        )


class DeleteTask(RetrieveDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    lookup_field = "pk"  # Adjust to your actual primary key field name

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
        except Exception as e:
            print(f"Error deleting task: {str(e)}")
            return Response(
                {"error": "Failed to delete task."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {"message": "Task deleted successfully.", "data": response.data},
            status=status.HTTP_200_OK,
        )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        task = self.get_object()
        summary = TaskSummary.objects.get_or_create(task=task)[0]
        serializer = TaskSummarySerializer(summary)
        return Response(serializer.data)


class TaskSummaryViewSet(viewsets.ModelViewSet):
    queryset = TaskSummary.objects.all()
    serializer_class = TaskSummarySerializer


class UserView(APIView):
    serializer_class = UserSerializer

    def get(self, request: HttpRequest, user_id: int | None = None) -> JsonResponse:
        if user_id:
            try:
                user = get_object_or_404(User, id=user_id)
            except Http404:
                return JsonResponse(
                    {"error": "User does not exist with this id"}, status=400
                )
        else:
            user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> JsonResponse:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserTaskList(APIView):
    """
    API endpoint to retrieve tasks associated with the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        try:
            # Retrieve tasks associated with the authenticated user
            user_tasks = Task.objects.filter(assigned_users=request.user)

            # Serialize the tasks
            serializer = TaskSerializer(user_tasks, many=True)

            # Return the serialized data as a JSON response
        except Exception as e:
            error_message = str(e)
            return Response(
                {"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id: int):
        try:
            # Retrieve the task detail for the given task_id
            task_detail = Task.objects.get(id=task_id)
        except Exception as e:
            # Handle the case where the task with the given task_id does not exist
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the task detail
        serializer = TaskSerializer(task_detail)

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)


class InviteUsers(APIView):
    def post(self, request):
        try:
            user_email = request.data.get("email")
            task_id = request.data.get("id")

            user = User.objects.get(email=user_email)
            task = Task.objects.get(id=task_id)

            # Add the user to the task's assigned_users
            task.assigned_users.add(user)

            return Response(
                {"message": f"User {user_email} added to Task {task_id} successfully"},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Task.DoesNotExist:
            return Response(
                {"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AllUserEmail(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserEmailSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
