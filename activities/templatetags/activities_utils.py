from django import template
from clubs import utils
from clubs.models import Club
from activities import utils
from forms_builder.forms.models import Form

register = template.Library()

@register.filter
def show_activity_forms(activity, user):
    if utils.forms_editor_check(user, activity):
        return True
    else:
        return Form.objects.published().filter(content_type__model="activity", object_id=activity.pk).exists()

@register.filter
def can_read_reviews(user, activity):
    return utils.can_read_reviews(user, activity)

@register.filter
def can_view_invitation_list(user, activity):
    return utils.can_view_invitation_list(user, activity)
