from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

from questions.views import QuestionListView
from questions.models import Question


class QuestionListViewTests(TestCase):
    def setUp(self):
        self.url = reverse("home")
        self.response = self.client.get(self.url)
        self.user = User.objects.create_user(username="hari", password="1234")
        self.client.login(username="hari", password="1234")
        for i in range(15):
            question = Question(
                title=f"question{i}",
                description=f"description{i}",
                created_by=self.user,
            )
            question.save()

    def test_status_code_is_200(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_question_list_function(self):
        view = resolve("/")
        self.assertEquals(view.func.view_class, QuestionListView)

    def test_view_is_paginated(self):
        response = self.client.get(self.url)
        self.assertTrue(response.context["is_paginated"])

    def test_paginator_return_given_number_of_questions(self):
        response = self.client.get(self.url)
        object_list = response.context["object_list"]
        self.assertEquals(object_list.count(), 10)
