from django.urls import path

from task_manager import views

urlpatterns = [
    path("", views.index, name="index"),
    path("teams/", views.TeamListView.as_view(), name="team_list"),
    path("teams/create/", views.TeamCreateView.as_view(), name="team_create")
]
app_name = "task_manager"
