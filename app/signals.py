from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, TaskSummary


@receiver(post_save, sender=Task)
def update_task_summary(sender, instance, created, **kwargs):
    """
    Signal handler to update the TaskSummary whenever a Task is updated.
    """
    if created:
        # If the Task is just created, create a new TaskSummary
        TaskSummary.objects.create(task=instance)
    else:
        # If the Task is updated, update the TaskSummary
        task_summary, created = TaskSummary.objects.get_or_create(task=instance)
        # Update the summary as needed based on your logic
        task_summary.summary = f"Summary for task: {instance.title}"
        task_summary.save()
