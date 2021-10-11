from django import template
from django.apps import apps

register = template.Library()

UPVOTED = 1
DOWNVOTED = -1
NOT_VOTED_YET = 0


@register.simple_tag
def check_user_voted_this(model_name, object_id, user):
    model = apps.get_model(app_label="questions", model_name=model_name)
    object = model.objects.get(id=object_id)
    if user.is_authenticated:
        user_votes_up = object.votes.user_ids(0)
        user_votes_down = object.votes.user_ids(1)
        check = {"user_id": user.id}

        if check in user_votes_up.values("user_id"):
            status = UPVOTED

        elif check in user_votes_down.values("user_id"):
            status = DOWNVOTED

        else:
            status = NOT_VOTED_YET
    else:
        status = NOT_VOTED_YET

    return status
