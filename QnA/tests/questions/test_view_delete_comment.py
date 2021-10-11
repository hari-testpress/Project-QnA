from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from questions.models import Question, Comment


class QuestionDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hari", password="1234")
        self.client.login(username="hari", password="1234")
        self.question = Question(
            title="title", description="description", created_by=self.user
        )
        self.question.save()
        self.comment = Comment(
            target=self.question,
            text="this is an answer",
            created_by=self.user,
        )
        self.comment.save()
        self.url = reverse(
            "questions:delete-comment",
            args=[self.question.id, self.comment.id],
        )
        self.response = self.client.get(self.url)
        self.success_url = reverse(
            "questions:question_detail", args=[self.question.id]
        )

    def test_page_serves_successfully(self):
        self.assertEquals(self.response.status_code, 200)

    def test_page_returns_404_for_the_non_creator(self):
        user = User.objects.create_user(username="nathan", password="1234")
        user.save()
        self.client.login(username="nathan", password="1234")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 404)

    def test_view_delete_the_comment_from_the_database(self):
        self.client.post(self.url, {})
        self.assertFalse(Comment.objects.exists())

    def test_unauthorized_user_redirected_to_the_login_page(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")
