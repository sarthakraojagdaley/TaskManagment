from django.contrib import admin
from .models import Task, TaskSummary

# Register your models here.


@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "due_date",
        "display_assigned_users",
        "status",
    )

    def display_assigned_users(self, obj):
        return ", ".join([user.username for user in obj.assigned_users.all()])

    display_assigned_users.short_description = "Assigned Users"


@admin.register(TaskSummary)
class AdminTaskSummry(admin.ModelAdmin):
    list_display = ("task", "summary")
