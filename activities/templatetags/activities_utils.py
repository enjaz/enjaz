from django import template
from clubs import utils
from clubs.models import Club
from activities.utils import forms_editor_check
from forms_builder.forms.models import Form


register = template.Library()

@register.filter
def show_activity_forms(activity, user):
    if forms_editor_check(user, activity):
        return True
    else:
        return Form.objects.published().filter(content_type__model="activity", object_id=activity.pk).exists()
