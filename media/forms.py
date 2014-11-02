# -*- coding: utf-8  -*-
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from clubs.utils import get_media_center

from media.models import FollowUpReport, Story, StoryReview, Article, ArticleReview, CustomTask, TaskComment, Poll, \
    PollResponse, WHAT_IF, HUNDRED_SAYS

# A nice trick to display full names instead of usernames
# Check: http://stackoverflow.com/questions/16369403/foreign-key-and-select-field-value-in-admin-interface
class CustomUserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        try:
            return obj.student_profile.get_ar_full_name()
        except ObjectDoesNotExist:
            return obj

class FollowUpReportForm(ModelForm):
    class Meta:
        model = FollowUpReport
        fields = ['description', 'start_date', 'end_date',
                  'start_time', 'end_time', 'location',
                  'organizer_count', 'participant_count',
                  'announcement_sites', 'images', 'notes']

class StoryForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': u'العنوان'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '18', 'placeholder': u'النص'}))
    class Meta:
        model = Story
        fields = ['title', 'text']

class StoryReviewForm(ModelForm):
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': u'الملاحظات'}))
    approve = forms.BooleanField(label=u"اعتمد التغطية.", required=False)
    class Meta:
        model = StoryReview
        fields = ['notes', 'approve']

class ArticleForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': u'العنوان'}))
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '18', 'placeholder': u'النص'}))

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        text = cleaned_data.get("text")
        attachment = cleaned_data.get("attachment")

        if not (text or attachment):
            # If both text and attachment are empty, raise an error
            msg = u"يرجى كتابة نص أو رفع ملف مرفق."
            raise forms.ValidationError(msg)
        elif text and attachment:
            # On the other hand, if both are full raise an error
            msg = u"يرجى كتابة نص أو رفع ملف مرفق. لا يمكن القيام بالاثنين معًَا."
            raise forms.ValidationError(msg)

        return cleaned_data

    class Meta:
        model = Article
        fields = ['title', 'text', 'author_photo', 'attachment']

class ArticleReviewForm(ModelForm):
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': u'الملاحظات'}))
    approve = forms.BooleanField(label=u"اعتمد المقال.", required=False)
    class Meta:
        model = ArticleReview
        fields = ['notes', 'approve']

class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs = {'class': 'autogrow'}
    assignee = CustomUserChoiceField(queryset=User.objects.filter(memberships=get_media_center()))
    class Meta:
        model = CustomTask
        fields = ['assignee', 'title', 'description', 'due_date']

class TaskCommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskCommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'class': 'form-control autogrow', 'placeholder': u"أضف تعليقًا..."}
    class Meta:
        model = TaskComment
        fields = ['body']


class PollForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get("poll_type") == WHAT_IF:
            self.choices = forms.HiddenInput()
        super(PollForm, self).__init__(*args, **kwargs)

    poll_type = forms.HiddenInput()

    class Meta:
        model = Poll
        exclude = ('date_created', 'creator')


class PollResponseForm(ModelForm):
    def __init__(self, poll_type=None, *args, **kwargs):
        if poll_type:
            if poll_type == WHAT_IF:
                self.choice = forms.HiddenInput()
        else:
            raise ValueError("Please specify the poll type.")
        super(PollResponseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PollResponse
        exclude = ('poll', 'user', 'date')