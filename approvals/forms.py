from django import forms
from django.forms.models import inlineformset_factory

from approvals.models import ActivityRequest, EventRequest, ActivityRequestReview


class ActivityCreateRequestForm(forms.ModelForm):
    class Meta:
        model = ActivityRequest
        fields = ['name']


class ActivityUpdateRequestForm(forms.ModelForm):
    class Meta:
        model = ActivityRequest
        fields = '__all__'


class ActivityRequestResponseForm(forms.ModelForm):
    class Meta:
        model = ActivityRequestReview
        fields = '__all__'


EventRequestFormSet = inlineformset_factory(ActivityRequest, EventRequest, fields='__all__', extra=1)
