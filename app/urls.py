from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet,
    TaskSummaryViewSet,
    UserView,
    UserTaskList,
    TaskDetail,
    UpdateTask,
    AddTask,
    DeleteTask,
    InviteUsers,
    AllUserEmail
)

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"task-summaries", TaskSummaryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("user/", UserView.as_view()),
    path("user/<int:user_id>", UserView.as_view()),
    path("user-task/", UserTaskList.as_view()),
    path("task-detail/<int:task_id>", TaskDetail.as_view()),
    path("update-task/<int:pk>", UpdateTask.as_view()),
    path("add-task/", AddTask.as_view()),
    path("delete-task/<int:pk>", DeleteTask.as_view()),
    path("invite-users/", InviteUsers.as_view()),
    path("users-email/",AllUserEmail.as_view())

]
