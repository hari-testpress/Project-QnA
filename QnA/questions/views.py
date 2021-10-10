# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import QuestionFilter

from .models import Answer, Question


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


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ["title", "description", "tags"]
    template_name = "question_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = "question_update.html"
    fields = ["title", "description", "tags"]
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = "question_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class AnswerCreateView(LoginRequiredMixin, CreateView):
    http_method_names = ["post"]
    model = Answer
    fields = ["text"]

    def get_success_url(self):
        return reverse_lazy(
            "questions:question_detail", args=[self.kwargs["question_id"]]
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question = Question.objects.get(
            id=self.kwargs["question_id"]
        )
        self.object.created_by = self.request.user
        return super().form_valid(form)


class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    model = Answer
    fields = ["text"]
    template_name = "answer_update.html"
    context_object_name = "answer"

    def get_success_url(self):
        return reverse_lazy(
            "questions:question_detail", args=[self.object.question.id]
        )


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer
    template_name = "question_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "questions:question_detail", args=[self.kwargs["question_id"]]
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)
