from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

from questions.views import QuestionCreateView
from questions.models import Question


class QuestionCreateTests(TestCase):
    def setUp(self):
        self.url = reverse("questions:create-question")
        self.user = User.objects.create_user(username="hari", password="1234")
        self.client.login(username="hari", password="1234")
        self.response = self.client.get(self.url)
        self.home_url = reverse("home")

    def test_page_generated_sucessfully(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_view_class_correctly(self):
        view = resolve(self.url)
        self.assertEquals(view.func.view_class, QuestionCreateView)

    def test_response_contains_form(self):
        response = self.client.get(self.url)
        self.assertTrue(response.context["form"])

    def test_valid_form_submission_stores_question(self):
        response = self.client.post(
            self.url,
            {"title": "title", "description": "description", "tags": "hello"},
            follow=True,
        )
        self.assertTrue(Question.objects.exists())
        self.assertEquals(response.status_code, 200)

    def test_valid_form_submission_redirect_the_user_to_the_home_page(self):
        response = self.client.post(
            self.url,
            {"title": "title", "description": "description", "tags": "hell0"},
        )
        self.assertRedirects(response, self.home_url)

    def test_authorized_user_only_can_create_a_question(self):
        response = self.client.post(
            self.url,
            {"title": "title", "description": "description", "tags": "hell0"},
        )
        self.assertEquals(response.status_code, 302)

    def test_unauthorized_user_redirected_to_the_login_page(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response, "/accounts/login/?next=%2Fquestions%2Fcreate-question%2F"
        )
