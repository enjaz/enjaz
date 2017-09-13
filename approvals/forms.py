from django import forms
from django.forms.models import inlineformset_factory

from approvals.models import ActivityRequest, EventRequest, ActivityRequestReview, RequirementRequest, FileAttachment, \
    DepositoryItemRequest


class ActivityCreateRequestForm(forms.ModelForm):
    class Meta:
        model = ActivityRequest
        exclude = ['activity', 'submission_datetime', 'submitter', 'is_update_request']


class ActivityUpdateRequestForm(forms.ModelForm):
    class Meta:
        model = ActivityRequest
        fields = '__all__'


class ActivityRequestResponseForm(forms.ModelForm):
    class Meta:
        model = ActivityRequestReview
        fields = '__all__'


EventRequestFormSet = inlineformset_factory(ActivityRequest, EventRequest, fields='__all__', extra=1)

DepositoryItemRequestFormSet = inlineformset_factory(
    ActivityRequest, DepositoryItemRequest, fields=['name', 'quantity'], extra=1,
    widgets={'name': forms.TextInput(attrs={'class': 'depository-item-request-autocomplete text-right'})},
)

RequirementRequestFormSet = inlineformset_factory(ActivityRequest, RequirementRequest, fields='__all__', extra=1)

FileAttachmentFormSet = inlineformset_factory(ActivityRequest, FileAttachment, fields='__all__', extra=1)
