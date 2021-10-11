from questions.models import Question
import django_filters
from taggit.forms import TagField


class TagFilter(django_filters.CharFilter):
    field_class = TagField

    # def __init__(self, *args, **kwargs):
    #     kwargs.setdefault("lookup_expr", "in")
    #     super().__init__(*args, **kwargs)


class QuestionFilter(django_filters.FilterSet):
    tags = TagFilter(field_name="tags__name", lookup_expr="in")

    class Meta:
        model = Question
        fields = ["created"]
