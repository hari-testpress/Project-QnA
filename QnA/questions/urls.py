from django.urls import path
from . import views

app_name = "questions"
urlpatterns = [
    path(
        "<int:pk>/", views.QuestionDetailView.as_view(), name="question_detail"
    ),
    path(
        "create-question/",
        views.QuestionCreateView.as_view(),
        name="create-question",
    ),
    path(
        "<int:pk>/edit",
        views.QuestionUpdateView.as_view(),
        name="edit-question",
    ),
    path(
        "<int:pk>/delete",
        views.QuestionDeleteView.as_view(),
        name="delete",
    ),
    path(
        "<int:question_id>/create-answer",
        views.AnswerCreateView.as_view(),
        name="create-answer",
    ),
]
