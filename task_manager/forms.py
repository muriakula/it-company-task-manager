from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField

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
