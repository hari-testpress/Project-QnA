# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from typing import Text

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)

from taggit.managers import TaggableManager
from vote.models import VoteModel


class Common(VoteModel, models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Comment(Common, models.Model):
    text = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    target = GenericForeignKey()


class Question(Common, models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    tags = TaggableManager()
    comments = GenericRelation(Comment)


class Answer(Common, models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.TextField()
    comments = GenericRelation(Comment)
