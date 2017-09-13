# coding=utf-8
from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from approvals.models import ActivityRequest, EventRequest, ActivityRequestReview, RequirementRequest, FileAttachment, \
    DepositoryItemRequest


class ActivityCreateRequestForm(forms.ModelForm):
    class Meta:
        model = ActivityRequest
        exclude = ['activity', 'submission_datetime', 'submitter', 'is_update_request']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'autogrow', 'rows': '3'}),
            'goals': forms.Textarea(attrs={'class': 'autogrow', 'rows': '3'}),
            'inside_collaborators': forms.Textarea(attrs={'class': 'autogrow', 'rows': '3'}),
            'outside_collaborators': forms.Textarea(attrs={'class': 'autogrow', 'rows': '3'}),
        }


class ActivityUpdateRequestForm(forms.ModelForm):
    class Meta:
        model = ActivityRequest
        fields = '__all__'


class ActivityRequestResponseForm(forms.ModelForm):
    class Meta:
        model = ActivityRequestReview
        fields = '__all__'


EventRequestFormSet = inlineformset_factory(
    ActivityRequest, EventRequest, fields='__all__', extra=1,
    widgets={
        'label': forms.TextInput(attrs={'placeholder': _(u"صف الفعالية بعنوان قصير مناسب..."), 'class': 'input-lg'}),
        'description': forms.Textarea(attrs={'placeholder': _(u"صف الفعالية بشيء من التفصيل..."), 'rows': '6', 'class': 'autogrow'}),
        'date': forms.TextInput(attrs={'placeholder': _(u"اختر التاريخ من القائمة...")}),
        'location': forms.TextInput(attrs={'placeholder': _(u"اسم المبنى؟ رقم القاعة؟ إلخ...")})
    },
    labels={
        'label': _(u"ما عنوان هذه الفعاليّة؟"),
        'description': _(u"ما طبيعة و محتوى هذه الفعاليّة؟"),
        'date': _(u"في أي يوم ستقام هذه الفعاليّة؟"),
        'start_time': _(u"في أي ساعة ستبدأ الفعاليّة؟"),
        'end_time': _(u"في أي ساعة ستنتهي؟"),
        'location': _(u"أين ستقام الفعاليّة؟"),
    },
)

DepositoryItemRequestFormSet = inlineformset_factory(
    ActivityRequest, DepositoryItemRequest, fields=['name', 'quantity'], extra=1,
    widgets={'name': forms.TextInput(attrs={'class': 'depository-item-request-autocomplete text-right'})},
)

RequirementRequestFormSet = inlineformset_factory(ActivityRequest, RequirementRequest, fields='__all__', extra=1)

FileAttachmentFormSet = inlineformset_factory(ActivityRequest, FileAttachment, fields='__all__', extra=1)
