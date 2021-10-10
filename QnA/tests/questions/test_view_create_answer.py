from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

from questions.models import Question


class AnswerCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hari", password="1234")
        self.client.login(username="hari", password="1234")
        self.question = Question(
            title="title", description="description", created_by=self.user
        )
        self.question.save()
        self.url = reverse("questions:create-answer", args=[self.question.id])
        self.response = self.client.get(self.url)
        self.success_url = reverse(
            "questions:question_detail", args=[self.question.id]
        )

    def test_unauthorized_user_redirected_to_the_login_page(self):
        self.client.logout()
        response = self.client.post(self.url, {})
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_view_add_answer_to_the_question(self):
        self.client.post(self.url, {"text": "answer"})
        self.assertTrue(self.question.answers.exists())

    def test_valid_form_submission_redirect_to_the_detail_page(self):
        response = self.client.post(self.url, {"text": "answer"})
        self.assertRedirects(response, self.success_url)
