from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Worker


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name"
        )


class WorkerForm(UserChangeForm):
    class Meta:
        model = Worker
        exclude = ["user_permissions", "groups", "is_superuser", "last_login", "is_staff", "date_joined"]