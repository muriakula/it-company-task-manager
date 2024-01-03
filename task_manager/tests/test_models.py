from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from task_manager.models import TaskType, Position, Team, Worker, VisitorCounter, increment_unique_visitors


class ModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Position Test")
        self.task_type = TaskType.objects.create(name="TaskType Test")
        self.team = Team.objects.create(name="Team Test")
        self.worker1 = Worker.objects.create(
            username='john_doe',
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            position=self.position,
            team=self.team
        )


class TaskTypeModelTest(ModelTest):
    def test_str_representation(self):
        self.assertEqual(str(self.task_type), self.task_type.name)


class PositionModelTest(ModelTest):
    def test_str_representation(self):
        self.assertEqual(str(self.position), self.position.name)


class TeamModelTest(ModelTest):
    def test_str_representation(self):
        self.assertEqual(str(self.team), self.team.name)


class WorkerModelTest(ModelTest):
    def test_str_representation(self):
        self.assertEqual(str(self.worker1), f"{self.worker1.first_name} "
                                            f"{self.worker1.last_name} "
                                            f"({self.worker1.position})")

    def test_save_method_does_not_overwrite_date_joined(self):
        existing_date_joined = timezone.now() - timezone.timedelta(days=365)
        worker = Worker(
            username='jane_doe',
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
            position=self.position,
            team=self.team,
            date_joined=existing_date_joined
        )
        self.assertEqual(worker.date_joined, existing_date_joined)
        worker.save()
        self.assertEqual(worker.date_joined, existing_date_joined)


class VisitorCounterModelTest(TestCase):
    def test_increment_unique_visitors_creates_counter_if_not_exists(self):
        VisitorCounter.objects.all().delete()
        increment_unique_visitors()
        self.assertEqual(VisitorCounter.objects.count(), 1)

    def test_increment_unique_visitors_increments_counter(self):
        VisitorCounter.objects.create(pk=1, count=0)
        initial_count = VisitorCounter.objects.get(pk=1).count
        increment_unique_visitors()
        updated_count = VisitorCounter.objects.get(pk=1).count
        self.assertEqual(updated_count, initial_count + 1)
