"""QnA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path,include
from questions import views

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("questions/", include("questions.urls", namespace="questions")),
    path(
        "<str:model_name>/<int:object_id>/upvote", views.upvote, name="upvote"
    ),
    path(
        "<str:model_name>/<int:object_id>/downvote",
        views.downvote,
        name="downvote",
    ),
    path(
        "<str:model_name>/<int:object_id>/undo-vote",
        views.undo_vote,
        name="undo-vote",
    ),
    path("", views.QuestionListView.as_view(), name="home"),
]
