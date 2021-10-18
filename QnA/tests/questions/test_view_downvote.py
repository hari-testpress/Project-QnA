from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from questions.models import Question, Answer, Comment


class DownvoteTestMixin:
    def test_unauthorized_user_redirected_to_the_login_page(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_page_serves_successfully(self):
        self.assertEquals(self.response.status_code, 302)

    def test_user_id_is_exists_in_voted_list(self):
        self.assertIn(
            self.user.id,
            self.object.votes.user_ids(1).values_list("id", flat=True),
        )

    def test_downvote_count_increase_after_downvote(self):
        self.assertEquals(self.object.num_vote_down, 1)

    def test_response_redirects_to_the_question_detail_page(self):
        self.assertRedirects(self.response, self.success_url)


class QuestionUpvoteTests(DownvoteTestMixin, TestCase):
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
            "downvote",
            args=["question", self.question.id],
        )
        self.success_url = reverse(
            "questions:question_detail", args=[self.question.id]
        )
        self.response = self.client.get(self.url)
        self.object = Question.objects.get(id=self.question.id)


class AnswerUpvoteTest(DownvoteTestMixin, TestCase):
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
            "downvote",
            args=["answer", self.answer.id],
        )
        self.success_url = reverse(
            "questions:question_detail", args=[self.question.id]
        )
        self.response = self.client.get(self.url)
        self.object = Answer.objects.get(id=self.answer.id)


class CommentUpvoteTest(DownvoteTestMixin, TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hari", password="1234")
        self.client.login(username="hari", password="1234")
        self.question = Question(
            title="title", description="description", created_by=self.user
        )
        self.question.save()
        self.comment = Comment(
            target=self.question,
            text="this is an comment",
            created_by=self.user,
        )
        self.comment.save()
        self.url = reverse(
            "downvote",
            args=["comment", self.comment.id],
        )
        self.success_url = reverse(
            "questions:question_detail", args=[self.question.id]
        )
        self.response = self.client.get(self.url)
        self.object = Comment.objects.get(id=self.comment.id)
