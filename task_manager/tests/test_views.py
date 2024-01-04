from django.test import TestCase

from task_manager.models import Position, Team, Worker


class TeamListViewTest(TestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name="Team1")
        self.team2 = Team.objects.create(name="Team2")
        self.team3 = Team.objects.create(name="Team3")
        self.response = self.client.get("/teams/")

    def test_view_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "pages/team_list.html")

    def test_view_displays_team_list(self):
        self.assertContains(self.response, "Team1")
        self.assertContains(self.response, "Team2")
        self.assertContains(self.response, "Team3")

    def test_search_form_displayed(self):
        self.assertContains(self.response, "Search")

    def test_search_works(self):
        response = self.client.get("/teams/", {"name": "2"})
        self.assertContains(response, "Team2")
        self.assertNotContains(response, "Team1")
        self.assertNotContains(response, "Team3")


class WorkerListViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get("/workers/")
        self.position = Position.objects.create(name="Position Test")
        self.team = Team.objects.create(name="Team Test")
        self.worker1 = Worker.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            position=self.position,
            team=self.team,
        )
        self.worker2 = Worker.objects.create(
            username="jane_doe",
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            position=self.position,
            team=self.team,
        )

    def test_view_url_exists(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "pages/workers_list.html")

    def test_view_displays_workers_list(self):
        response = self.client.get("/workers/", {"search_query": ""})
        self.assertContains(response, "John")
        self.assertContains(response, "Jane")

    def test_search_form_displayed(self):
        self.assertContains(self.response, "Search")

    def test_search_works(self):
        response = self.client.get("/workers/", {"search_query": "Jane"})
        self.assertContains(response, "Jane")
        self.assertNotContains(response, "John")
