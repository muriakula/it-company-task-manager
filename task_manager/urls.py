from django.urls import path

from task_manager import views

urlpatterns = [
    path("", views.index, name="index"),
    path("teams/", views.TeamListView.as_view(), name="team_list"),
    path("teams/create/", views.TeamCreateView.as_view(), name="team_create"),
    path("teams/<int:pk>/update/", views.TeamUpdateView.as_view(), name="team_update"),
    path("teams/<int:pk>/delete/", views.TeamDeleteView.as_view(), name="team_delete"),
    path("workers/", views.WorkerListView.as_view(), name="worker_list"),
    path("workers/<int:pk>", views.WorkerDetailView.as_view(), name="worker_detail"),
    path("workers/<int:pk>/update", views.WorkerUpdateView.as_view(), name="worker_update"),
    path("workers/create/", views.WorkerCreateView.as_view(), name="worker_create"),
    path("workers/<int:pk>/delete", views.WorkerDeleteView.as_view(), name="worker_delete"),
    path("positions/", views.PositionListView.as_view(), name="position_list")
]
app_name = "task_manager"
