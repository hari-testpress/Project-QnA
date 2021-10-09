# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import QuestionFilter

from .models import Question


def index(request):
    return render(request, "base.html")


class QuestionListView(ListView):
    model = Question
    template_name = "question_list.html"
    context_object_name = "questions"
    paginate_by = 10

    def get_queryset(self):
        question_list = super().get_queryset()
        filter = QuestionFilter(self.request.GET, queryset=question_list)
        return filter.qs


class QuestionDetailView(DetailView):
    model = Question
    template_name = "question_detail_view.html"
    context_object_name = "question"

    def get_queryset(self):
        return super().get_queryset()


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ["title", "description", "tags"]
    template_name = "question_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)
