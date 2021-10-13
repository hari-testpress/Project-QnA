from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

from questions.models import Question, Answer, Comment
from questions.views import EditAnswerCommentView, EditQuestionCommentView


class EditCommentMixin:
    def test_page_serves_correctly_for_the_creator(self):
        self.assertEquals(self.response.status_code, 200)

    def test_page_returns_404_for_the_non_creator(self):
        user = User.objects.create_user(username="nathan", password="1234")
        user.save()
        self.client.login(username="nathan", password="1234")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 404)

    def test_response_contains_form(self):
        response = self.client.get(self.url)
        self.assertTrue(response.context["form"])

    def test_unauthorized_user_redirected_to_the_login_page(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_updated_the_comment_correctly(self):
        self.client.post(self.url, {"text": "updated comment"})
        updated_answer = Comment.objects.get(id=self.comment.id)
        self.assertEqual(updated_answer.text, "updated comment")


class EditTheCommentOnAnswerViewTests(EditCommentMixin, TestCase):
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
        self.comment = Comment(
            target=self.answer,
            text="this is an answer",
            created_by=self.user,
        )
        self.comment.save()
        self.url = reverse(
            "questions:edit-comment-on-the-answer",
            args=[self.question.id, self.answer.id, self.comment.id],
        )
        self.response = self.client.get(self.url)
        self.success_url = reverse(
            "questions:question_detail", args=[self.question.id]
        )

    def test_url_resolves_view_class_correctly(self):
        view = resolve(self.url)
        self.assertEquals(view.func.view_class, EditAnswerCommentView)


class EditTheCommentOnQuestionViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hari", password="1234")
        self.client.login(username="hari", password="1234")
        self.question = Question(
            title="title", description="description", created_by=self.user
        )
        self.question.save()
        self.comment = Comment(
            target=self.question,
            text="this is a comment",
            created_by=self.user,
        )
        self.comment.save()
        self.url = reverse(
            "questions:edit-comment-on-the-question",
            args=[self.question.id, self.comment.id],
        )
        self.response = self.client.get(self.url)
        self.success_url = reverse(
            "questions:question_detail", args=[self.question.id]
        )

    def test_url_resolves_view_class_correctly(self):
        view = resolve(self.url)
        self.assertEquals(view.func.view_class, EditQuestionCommentView)
