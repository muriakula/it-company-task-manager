from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View

from task_manager import models
from task_manager.forms import (WorkerForm,
                                WorkerCreationForm,
                                CustomAuthenticationForm,
                                TeamSearchForm,
                                WorkerSearchForm,
                                TaskSearchForm,
                                TaskForm,
                                AddWorkerForm)


# Create your views here.
def index(request):
    num_workers = models.Worker.objects.count()
    num_tasks = models.Task.objects.count()
    num_completed_tasks = models.Task.objects.filter(is_completed=True).count()
    num_teams = models.Team.objects.count()

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_completed_tasks": num_completed_tasks,
        "num_teams": num_teams
    }
    return render(request, 'pages/index.html', context=context)


class TeamListView(generic.ListView):
    model = models.Team
    context_object_name = "team_list"
    template_name = "pages/team_list.html"
    form_class = TeamSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form_class(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset


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
    form_class = WorkerSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form_class(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            search_query = form.cleaned_data.get("search_query")
            if search_query:
                queryset = queryset.filter(
                    Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
                )
        return queryset


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


class PositionCreateView(generic.CreateView):
    model = models.Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position_list")
    template_name = "pages/position_form.html"


class PositionUpdateView(generic.UpdateView):
    model = models.Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position_list")
    template_name = "pages/position_form.html"


class PositionDeleteView(generic.DeleteView):
    model = models.Position
    success_url = reverse_lazy("task_manager:position_list")
    template_name = "pages/position_confirm_delete.html"


class TaskTypeListView(generic.ListView):
    model = models.TaskType
    context_object_name = "task_type_list"
    template_name = "pages/task_type_list.html"


class TaskTypeCreateView(generic.CreateView):
    model = models.TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task_type_list")
    template_name = "pages/task_type_form.html"


class TaskTypeUpdateView(generic.UpdateView):
    model = models.TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task_type_list")
    template_name = "pages/task_type_form.html"


class TaskTypeDeleteView(generic.DeleteView):
    model = models.TaskType
    success_url = reverse_lazy("task_manager:task_type_list")
    template_name = "pages/task_type_confirm_delete.html"


class AuthSigninView(View):
    template_name = 'auth_signin.html'

    def get(self, request, *args, **kwargs):
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_manager:index')
        return render(request, self.template_name, {'form': form})


class TaskListView(generic.ListView):
    model = models.Task
    context_object_name = "task_list"
    template_name = "pages/task_list.html"
    form_class = TaskSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form_class(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            search_query = form.cleaned_data.get("search_query")
            if search_query:
                queryset = queryset.filter(
                    Q(task_type__name__icontains=search_query) | Q(name__icontains=search_query)
                )
        return queryset


class TaskCreateView(generic.CreateView):
    model = models.Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task_list")
    template_name = "pages/task_form.html"


class TaskUpdateView(generic.UpdateView):
    model = models.Task
    success_url = reverse_lazy("task_manager:task_list")
    template_name = "pages/task_form.html"
    form_class = TaskForm


class TaskDeleteView(generic.DeleteView):
    model = models.TaskType
    success_url = reverse_lazy("task_manager:task_type_list")
    template_name = "pages/task_confirm_delete.html"


class AddWorkerToTaskView(View):
    template_name = "pages/add_worker_to_task.html"
    success_url = reverse_lazy("task_manager:task_list")

    def get(self, request, task_id, *args, **kwargs):
        task = get_object_or_404(models.Task, id=task_id)
        form = AddWorkerForm(instance=task)
        return render(request, self.template_name, {'form': form, 'task': task})

    def post(self, request, task_id, *args, **kwargs):
        task = get_object_or_404(models.Task, id=task_id)
        form = AddWorkerForm(request.POST, instance=task)
        if form.is_valid():
            workers = form.cleaned_data['workers']
            task.workers.add(*workers)
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'task': task})
