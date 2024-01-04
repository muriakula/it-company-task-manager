from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)

from .models import Worker, Task, Team


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position", "first_name", "last_name"
        )


class WorkerForm(UserChangeForm):
    class Meta:
        model = Worker
        exclude = [
            "user_permissions",
            "groups",
            "is_superuser",
            "last_login",
            "is_staff",
            "date_joined",
        ]


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Worker
        fields = ["username", "password"]


class TeamSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )


class WorkerSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )


class TaskSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {"deadline": forms.DateInput(attrs={"type": "date"})}


class AddWorkerForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []

    def __init__(self, *args, **kwargs):
        super(AddWorkerForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance")

        self.fields["workers_no_team"] = forms.ModelMultipleChoiceField(
            queryset=Worker.objects.filter(team__isnull=True),
            widget=forms.CheckboxSelectMultiple,
            label="Workers without a Team",
            required=False,
        )

        teams = Team.objects.all()
        for team in teams:
            team_workers = Worker.objects.filter(team=team)
            field_name = f"workers_{team.id}"

            self.fields[field_name] = forms.ModelMultipleChoiceField(
                queryset=team_workers,
                widget=forms.CheckboxSelectMultiple,
                label=f"Workers in {team.name}",
                required=False,
            )

            if instance:
                initial_workers = instance.workers.filter(team=team)
                self.fields[field_name].initial = initial_workers

        self.fields["select_all_team"] = forms.BooleanField(
            required=False,
            initial=False,
            widget=forms.CheckboxInput(attrs={"class": "select-all-team"}),
        )

    def clean(self):
        cleaned_data = super().clean()

        workers_no_team = cleaned_data.get("workers_no_team", [])
        cleaned_data["workers"] = list(
            set(cleaned_data.get("workers", [])) | set(workers_no_team)
        )

        for team in Team.objects.all():
            field_name = f"workers_{team.id}"
            workers = cleaned_data.get(field_name, [])
            cleaned_data["workers"] += list(set(workers))

        return cleaned_data
