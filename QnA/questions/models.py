from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)

from model_utils.models import TimeStampedModel


class Comment(TimeStampedModel):
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    target = GenericForeignKey()


class Question(TimeStampedModel):
    title = models.CharField(max_length=90)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = GenericRelation(Comment)


class Answer(TimeStampedModel):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comments = GenericRelation(Comment)
