# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import Http404

from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.http import HttpResponseRedirect

from .filters import QuestionFilter

from .models import Answer, Question, Comment


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
    template_name = "answer_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "questions:question_detail", args=[self.kwargs["question_id"]]
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class CreateCommentMixin(LoginRequiredMixin, CreateView):
    model = Comment
    http_method_names = ["post"]
    fields = ["text"]

    def get_success_url(self):
        return reverse_lazy(
            "questions:question_detail", args=[self.kwargs["question_id"]]
        )


class CreateQuestionCommentView(CreateCommentMixin):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        question_id = self.kwargs.get("question_id")
        self.object.target = get_object_or_404(Question, id=question_id)
        self.object.created_by = self.request.user
        return super().form_valid(form)


class CreateAnswerCommentView(CreateCommentMixin):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        answer_id = self.kwargs.get("answer_id")
        self.object.target = get_object_or_404(Answer, id=answer_id)
        self.object.created_by = self.request.user
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "questions:question_detail", args=[self.kwargs["question_id"]]
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class EditQuestionCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ["text"]
    template_name = "comment_update.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["question"] = get_object_or_404(
            Question, id=self.kwargs.get("question_id")
        )
        return context

    def get_success_url(self):
        return reverse_lazy(
            "questions:question_detail", args=[self.kwargs["question_id"]]
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class EditAnswerCommentView(EditQuestionCommentView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["answer"] = get_object_or_404(
            Answer, id=self.kwargs.get("answer_id")
        )
        return context


class VoteMixin(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.model_name = kwargs.get("model_name")
        self.object = self.get_object()
        self.user_id = request.user.id
        return super().setup(request, *args, **kwargs)

    def get_object(self):
        if self.model_name not in ["question", "answer", "comment"]:
            raise Http404("Invalid request")
        model = apps.get_model("questions", self.model_name)
        return model.objects.get(id=self.kwargs["object_id"])

    def get_success_url(self):
        if self.model_name == "answer":
            question_id = self.object.question.id
        elif self.model_name == "comment":
            question_id = self.object.object_id
        else:
            question_id = self.object.id
        return reverse_lazy("questions:question_detail", args=[question_id])


UPVOTE = 0
DOWNVOTE = 1


class Upvote(VoteMixin):
    def get(self, request, *args, **kwargs):
        if self.object.votes.exists(self.user_id, UPVOTE):
            self.object.votes.delete(self.user_id)
        else:
            self.object.votes.up(self.user_id)
        return HttpResponseRedirect(self.get_success_url())


class Downvote(VoteMixin):
    def get(self, request, *args, **kwargs):
        if self.object.votes.exists(self.user_id, DOWNVOTE):
            self.object.votes.delete(self.user_id)
        else:
            self.object.votes.down(self.user_id)
        return HttpResponseRedirect(self.get_success_url())
