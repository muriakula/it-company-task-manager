from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager import models
from task_manager.forms import WorkerForm, WorkerCreationForm


# Create your views here.
def index(request):
    num_workers = models.Worker.objects.count()
    num_tasks = models.Task.objects.count()
    num_completed_tasks = models.Task.objects.filter(is_completed=True).count()

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_completed_tasks": num_completed_tasks
    }
    # Page from the theme
    return render(request, 'pages/index.html', context=context)


class TeamListView(generic.ListView):
    model = models.Team
    context_object_name = "team_list"
    template_name = "pages/team_list.html"


class TeamCreateView(generic.CreateView):
    model = models.Team
    fields = "__all__"
    success_url = reverse_lazy("task_manager:team_list")
    template_name = "pages/team_form.html"


class TeamUpdateView(generic.UpdateView):
    model = models.Team
    fields = "__all__"
    success_url = reverse_lazy("task_manager:team_list")
    template_name = "pages/team_form.html"


class TeamDeleteView(generic.DeleteView):
    model = models.Team
    success_url = reverse_lazy("task_manager:team_list")
    template_name = "pages/team_confirm_delete.html"


class WorkerListView(generic.ListView):
    model = models.Worker
    context_object_name = "workers_list"
    template_name = "pages/workers_list.html"


class WorkerDetailView(generic.DetailView):
    model = models.Worker
    queryset = models.Worker.objects.all()
    template_name = "pages/user-profile.html"


class WorkerCreateView(generic.CreateView):
    model = models.Worker
    form_class = WorkerCreationForm
    template_name = "pages/user-form.html"

    def get_success_url(self):
        return reverse_lazy("task_manager:worker_detail", args=[self.object.pk])


class WorkerUpdateView(generic.UpdateView):
    model = models.Worker
    form_class = WorkerForm
    template_name = "pages/user-form.html"

    def get_object(self, queryset=None):
        return models.Worker.objects.get(pk=self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy("task_manager:worker_detail", args=[self.object.pk])


class WorkerDeleteView(generic.DeleteView):
    model = models.Worker
    success_url = reverse_lazy("task_manager:worker_list")
    template_name = "pages/worker_confirm_delete.html"


class PositionListView(generic.ListView):
    model = models.Position
    context_object_name = "positions_list"
    template_name = "pages/positions_list.html"
