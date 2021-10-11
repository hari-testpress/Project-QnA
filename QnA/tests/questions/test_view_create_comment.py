from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from questions.models import Question, Answer, Comment


class PostCommentTestMixin:
    def test_view_stores_the_comment(self):
        self.client.post(self.url, {"text": "comment"})
        self.assertTrue(Comment.objects.exists())

    def test_unauthorized_user_redirected_to_the_login_page(self):
        self.client.logout()
        response = self.client.post(self.url, {})
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_valid_form_submission_redirect_to_the_detail_page(self):
        response = self.client.post(self.url, {"text": "comment"})
        self.assertRedirects(response, self.success_url)


class PostCommentOnAnswer(PostCommentTestMixin, TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hari", password="1234")
        self.client.login(username="hari", password="1234")
        self.question = Question(
            title="title", description="description", created_by=self.user
        )
        self.question.save()
        self.answer = Answer(
            question=self.question,
            text="this is an answer",
            created_by=self.user,
        )
        self.answer.save()
        self.url = reverse(
            "questions:post-comment-on-answer",
            args=[self.question.id, self.answer.id],
        )
        self.success_url = reverse(
            "questions:question_detail", args=[self.question.id]
        )


class PostCommentOnQuestion(PostCommentTestMixin, TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hari", password="1234")
        self.client.login(username="hari", password="1234")
        self.question = Question(
            title="title", description="description", created_by=self.user
        )
        self.question.save()
        self.url = reverse(
            "questions:post-comment-on-question", args=[self.question.id]
        )
        self.response = self.client.get(self.url)
        self.success_url = reverse(
            "questions:question_detail", args=[self.question.id]
        )
