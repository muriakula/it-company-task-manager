from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import ModelMultipleChoiceField

from .models import Worker, Task


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


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Worker
        fields = ['username', 'password']


class TeamSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"})
    )


class WorkerSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search"}
        )
    )


class TaskSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search"}
        )
    )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"})
        }


class AddWorkerForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []

    def __init__(self, *args, **kwargs):
        super(AddWorkerForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance")

        if instance:
            initial_workers = instance.workers.all()
            self.fields["workers"] = forms.ModelMultipleChoiceField(
                queryset=Worker.objects.all(),
                widget=forms.CheckboxSelectMultiple,
                initial=initial_workers,
            )
        else:
            self.fields["workers"] = forms.ModelMultipleChoiceField(
                queryset=Worker.objects.all(),
                widget=forms.CheckboxSelectMultiple,
            )

    def clean_workers(self):
        workers = self.cleaned_data.get("workers", [])
        instance = self.instance

        if instance:
            current_workers = instance.workers.all()

            removed_workers = current_workers.exclude(id__in=workers)

            instance.workers.remove(*removed_workers)

        return workers
