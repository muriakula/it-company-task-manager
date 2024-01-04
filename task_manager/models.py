from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("low", "Low Priority"),
        ("medium", "Medium Priority"),
        ("high", "High Priority"),
    )
    name = models.CharField(max_length=255, unique=False)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium",
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    task = models.ManyToManyField(Task, blank=True, related_name="workers")
    team = models.ForeignKey(Team, blank=True,
                             on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"

    def save(self, *args, **kwargs):
        if not self.date_joined:
            self.date_joined = timezone.now()
        super().save(*args, **kwargs)


class VisitorCounter(models.Model):
    count = models.IntegerField(default=0)


def increment_unique_visitors():
    counter, created = VisitorCounter.objects.get_or_create(pk=1)
    counter.count += 1
    counter.save()
