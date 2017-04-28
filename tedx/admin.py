from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from clubs.models import Team
from .models import Registration, Question, Choice, Game

class TEDxAuthenticationForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        team = Team.objects.get(code_name='tedx_2017_registration')
        is_tedx_team_member = team.members.filter(pk=user.pk).exists() or \
                              team.coordinator == user
        if not user.is_superuser and \
           not user.is_active and \
           not is_tedx_team_member:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
                )

class TEDxAdmin(admin.sites.AdminSite):
    login_form = TEDxAuthenticationForm

    def has_permission(self, request):
        team = Team.objects.get(code_name='tedx_2017_registration')
        is_tedx_team_member = team.members.filter(pk=request.user.pk).exists() or \
                              team.coordinator == request.user
        return is_tedx_team_member or \
               request.user.is_superuser

class QuestionAdmin(admin.ModelAdmin):
    fields = ['title','question_text']

class ChoiceAdmin(admin.ModelAdmin):
    fields = ['title','choice_text','question','next_question','flag']

tedx_admin = TEDxAdmin("TEDx Admin")
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Game)
tedx_admin.register(Registration)
admin.site.register(Registration)
