from django.shortcuts import render

from task_manager import models


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
