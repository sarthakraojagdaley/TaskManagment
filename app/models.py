from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField(blank=True)
    assigned_users = models.ManyToManyField(
        User, related_name="assigned_tasks", blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("TODO", "To Do"),
            ("IN_PROGRESS", "In Progress"),
            ("COMPLETED", "Completed"),
        ],
    )


class TaskSummary(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    summary = models.TextField()
