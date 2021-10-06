# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from questions.models import Question, Answer, Comment

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
