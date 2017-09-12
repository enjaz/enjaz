from django import template
from teams import utils
from forms_builder.forms.models import Form

register = template.Library()

@register.filter
def show_team_forms(team, user):
    if utils.forms_editor_check(user, team):
        return True
    else:
        return Form.objects.published().filter(content_type__model="team", object_id=team.pk).exists()
