# coding=utf-8
from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from approvals.models import ActivityRequest, EventRequest, ActivityRequestReview, RequirementRequest, FileAttachment, \
    DepositoryItemRequest, ActivityRequestComment


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


class EventRequestForm(forms.ModelForm):
    label = forms.CharField(
        label=_(u"ما عنوان هذه الفعاليّة؟"),
        widget=forms.TextInput(attrs={'placeholder': _(u"صف الفعالية بعنوان قصير مناسب..."), 'class': 'input-lg'}),
    )
    description = forms.CharField(
        label=_(u"ما طبيعة و محتوى هذه الفعاليّة؟"),
        widget=forms.Textarea(attrs={'placeholder': _(u"صف لنا الفعالية بشيء من التفصيل..."), 'rows': '6', 'class': 'autogrow'}),
    )
    date = forms.DateField(
        label=_(u"في أي يوم ستقام هذه الفعاليّة؟"),
        widget=forms.TextInput(attrs={'placeholder': _(u"اختر التاريخ من القائمة...")}),
    )
    start_time = forms.TimeField(
        label=_(u"في أي ساعة ستبدأ الفعاليّة؟"),
        input_formats=("%I:%M %p", "%H:%M:%S", "%H:%M"),
    )
    end_time = forms.TimeField(
        label=_(u"في أي ساعة ستنتهي؟"),
        input_formats=("%I:%M %p", "%H:%M:%S", "%H:%M"),
    )
    location = forms.CharField(
        label=_(u"أين ستقام الفعاليّة؟"),
        widget=forms.TextInput(attrs={'placeholder': _(u"اسم المبنى؟ رقم القاعة؟ إلخ...")}),
    )

    class Meta:
        model = EventRequest
        fields = '__all__'


EventRequestFormSet = inlineformset_factory(ActivityRequest, EventRequest, form=EventRequestForm, extra=1)

DepositoryItemRequestFormSet = inlineformset_factory(
    ActivityRequest, DepositoryItemRequest, fields=['name', 'quantity'], extra=1,
    widgets={'name': forms.TextInput(attrs={'class': 'depository-item-request-autocomplete text-right'})},
)

RequirementRequestFormSet = inlineformset_factory(ActivityRequest, RequirementRequest, fields='__all__', extra=1)

FileAttachmentFormSet = inlineformset_factory(ActivityRequest, FileAttachment, fields='__all__', extra=1)


class ActivityRequestCommentForm(forms.ModelForm):
    text = forms.CharField(
        label=_(u"أضف تعليقًا"),
        widget=forms.Textarea(attrs={'rows': '3', 'class': 'autogrow', 'placeholder': _(u"تعليقك...")}),
    )

    class Meta:
        model = ActivityRequestComment
        fields = ['text']


class ActivityRequestReviewForm(forms.ModelForm):

    class Meta:
        model = ActivityRequestReview
        fields = [
            'submitter_team',  # temporary during development
            'is_approved',
        ]
