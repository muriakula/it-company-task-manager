from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    groups = models.ManyToManyField(Group, related_name="team")
    user_permissions = models.ManyToManyField(Permission, related_name="workers_permissions")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"

    def save(self, *args, **kwargs):
        if not self.date_joined:
            self.date_joined = timezone.now()
        super().save(*args, **kwargs)


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    team_members = models.ManyToManyField(Worker, related_name="team_members")


class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
    )
    name = models.CharField(max_length=255, unique=False)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    team = models.ManyToManyField(Worker, related_name="teams")
    assignees = models.ManyToManyField(Worker, related_name="workers")


@receiver(pre_save, sender=Task)
def add_workers_from_team(sender, instance, **kwargs):
    if instance.team:
        instance.assignees.add(*instance.team.worker_set.all())
