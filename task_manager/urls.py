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
    path("positions/", views.PositionListView.as_view(), name="position_list"),
    path("positions/create/", views.PositionCreateView.as_view(), name="position_create"),
    path("positions/<int:pk>/update/", views.PositionUpdateView.as_view(), name="position_update"),
    path("positions/<int:pk>/delete/", views.PositionDeleteView.as_view(), name="position_delete"),
    path("tasktype/", views.TaskTypeListView.as_view(), name="task_type_list"),
    path("tasktype/create/", views.TaskTypeCreateView.as_view(), name="task_type_create"),
    path("tasktype/<int:pk>/update/", views.TaskTypeUpdateView.as_view(), name="task_type_update"),
    path("tasktype/<int:pk>/delete/", views.TaskTypeDeleteView.as_view(), name="task_type_delete"),
    path("tasks/", views.TaskListView.as_view(), name="task_list"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:task_id>/add_worker/", views.AddWorkerToTaskView.as_view(), name="add_worker_to_task"),
]
app_name = "task_manager"
