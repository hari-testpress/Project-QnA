# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView

from .models import Question


def index(request):
    return render(request, "base.html")


class QuestionListView(ListView):
    model = Question
    template_name = "question_list.html"
    context_object_name = "questions"
    paginate_by = 10
