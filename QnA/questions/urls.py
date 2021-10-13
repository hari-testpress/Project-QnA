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
]
