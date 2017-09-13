from django import forms
from django.forms.models import inlineformset_factory

from approvals.models import ActivityRequest, EventRequest, ActivityRequestReview, RequirementRequest


class ActivityCreateRequestForm(forms.ModelForm):
    class Meta:
        model = ActivityRequest
        exclude = ['activity', 'submission_datetime', 'submitter', 'submitter_team', 'is_update_request']


class ActivityUpdateRequestForm(forms.ModelForm):
    class Meta:
        model = ActivityRequest
        fields = '__all__'


class ActivityRequestResponseForm(forms.ModelForm):
    class Meta:
        model = ActivityRequestReview
        fields = '__all__'


EventRequestFormSet = inlineformset_factory(ActivityRequest, EventRequest, fields='__all__', extra=1)

RequirementRequestFormSet = inlineformset_factory(ActivityRequest, RequirementRequest, fields='__all__', extra=3)
