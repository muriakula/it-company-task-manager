from datetime import datetime

from django import forms
from django.test import TestCase

from task_manager.forms import AddWorkerForm
from task_manager.models import Team, Worker, Position, Task, TaskType


class AddWorkerFormTest(TestCase):
    def setUp(self):
        self.task_type_instance = TaskType.objects.create(name="Test")
        self.task_instance = Task.objects.create(deadline=datetime.now(), task_type=self.task_type_instance)

    def test_init_fields(self):
        form = AddWorkerForm(instance=self.task_instance)
        self.assertIn("workers_no_team", form.fields)
        self.assertIn("select_all_team", form.fields)
        for team in Team.objects.all():
            field_name = f"workers_{team.id}"
            self.assertIn(field_name, form.fields)

        self.assertIsInstance(form.fields["workers_no_team"], forms.ModelMultipleChoiceField)
        self.assertIsInstance(form.fields["select_all_team"], forms.BooleanField)
        for team in Team.objects.all():
            field_name = f"workers_{team.id}"
            self.assertIsInstance(form.fields[field_name], forms.ModelMultipleChoiceField)
            if self.task_instance:
                initial_workers = self.task_instance.workers.filter(team=team)
                self.assertEqual(list(form.fields[field_name].initial), list(initial_workers))

    def test_clean_method(self):
        form_data = {
            "workers_no_team": [worker.id for worker in Worker.objects.filter(team__isnull=True)],
            "select_all_team": True
        }
        for team in Team.objects.all():
            form_data[f"workers_{team.id}"] = [worker.id for worker in Worker.objects.filter(team=team)]
        form = AddWorkerForm(instance=self.task_instance, data=form_data)
        self.assertTrue(form.is_valid())
        cleaned_data = form.clean()
        self.assertIsInstance(cleaned_data, dict)
        self.assertIn("workers", cleaned_data)
        self.assertEqual(len(cleaned_data["workers"]), Worker.objects.count())
