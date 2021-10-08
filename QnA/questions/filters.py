from questions.models import Question
import django_filters
from taggit.forms import TagField


class TagFilter(django_filters.CharFilter):
    field_class = TagField


class QuestionFilter(django_filters.FilterSet):
    tags = TagFilter(field_name="tags__name", lookup_expr="in")
    order = django_filters.OrderingFilter(fields=(("created", "created"),))

    class Meta:
        model = Question
        fields = ["created"]
