from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

from questions.views import QuestionDeleteView
from questions.models import Question


class QuestionDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hari", password="1234")
        self.client.login(username="hari", password="1234")
        self.question = Question(
            title="title", description="description", created_by=self.user
        )
        self.question.save()
        self.url = reverse("questions:delete", args=[self.question.id])
        self.response = self.client.get(self.url)
        self.home_url = reverse("home")

    def test_page_serves_successfully(self):
        self.assertEquals(self.response.status_code, 200)

    def test_page_returns_404_for_the_non_creator(self):
        user = User.objects.create_user(username="nathan", password="1234")
        user.save()
        self.client.login(username="nathan", password="1234")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 404)

    def test_view_delete_the_question_from_the_database(self):
        self.client.post(self.url, {})
        self.assertFalse(Question.objects.exists())

    def test_unauthorized_user_redirected_to_the_login_page(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response, "/accounts/login/?next=/questions/1/delete"
        )
