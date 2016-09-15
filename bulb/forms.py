# -*- coding: utf-8  -*-
import re

from django.contrib.auth.models import User
from django import forms
from dal import autocomplete
from tagging.fields import TagField

import accounts.utils
from bulb.models import Book, NeededBook, Request, Group, Session, Report, Membership, ReaderProfile, Recruitment
from bulb import utils

city_choices = (
    ('-', u'الرياض وجدة والأحساء'),
    ('R', u'الرياض فقط'),
    ('J', u'جدة فقط'),
    ('A', u'الأحساء فقط'),
)
gender_choices = (
    ('-', u'الطلاب والطالبات'),
    ('F', u'الطالبات'),
    ('M', u'الطلاب'),
    )

class CommonControl:
    def control_gender(self):
        # Modify the choice only if the user is not a superuser not a
        # Bulb coordinator.  This is a really, really, really stupid
        # default option, but it's just to make sure that people know
        # what are chosing.
        if self.user_gender == 'F':
            self.fields['gender'].initial = 'F'
            self.fields['gender'].choices = (
                ('-', u'الطلاب والطالبات'),
                ('F', u'الطالبات'),
                )
        elif self.user_gender == 'M':
            self.fields['gender'].initial = 'M'
            self.fields['gender'].choices = (
                ('-', u'الطلاب والطالبات'),
                ('M', u'الطلاب')
            )

class NeededBookForm(forms.ModelForm):
    class Meta:
        model = NeededBook
        fields = ['title', 'authors', 'description', 'cover', 'tags',
                  'category']

class GenericBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Remove is_publicly_owned field from ordinary users.
        user = kwargs.pop('user')
        super(GenericBookForm, self).__init__(*args, **kwargs)
        if user.is_superuser or \
           utils.is_bulb_coordinator_or_deputy(user) or \
           utils.is_bulb_member(user):
            del self.fields['is_publicly_owned']

class BookEditForm(GenericBookForm):
    """Form used to edit books. It allows changing contribution type from
       giving to lending."""
    tags = TagField()
    class Meta:
        model = Book
        fields = ['title', 'authors', 'edition', 'pages', 'condition',
                  'description', 'cover', 'tags', 'category',
                  'contribution', 'available_until', 'is_publicly_owned']

class BookGiveForm(GenericBookForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'edition', 'pages',
                  'condition', 'description', 'cover', 'tags',
                  'category', 'is_publicly_owned']

class BookLendForm(GenericBookForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'edition', 'pages', 'condition',
                  'description', 'cover', 'category', 'tags',
                  'available_until', 'is_publicly_owned']

class RequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(RequestForm, self).__init__(*args, **kwargs)
        if instance.book.contribution == 'L':
            self.fields['borrowing_end_date'].required = True

    def clean_delivery(self):
        # You know the "males and females are not supposed to meet"
        # bullshit? Yeah.
        data = self.cleaned_data['delivery']

        if not data:
            return data

        requester_gender = accounts.utils.get_user_gender(self.instance.requester)
        owner_gender = accounts.utils.get_user_gender(self.instance.book.submitter)
        if data == 'I' or  requester_gender != owner_gender:
            delivery = 'I'
        else:
            delivery = 'D'

        return delivery

    class Meta:
        model = Request
        fields = ['delivery', 'borrowing_end_date']
        widgets  = {'delivery': forms.HiddenInput()}

class GroupForm(forms.ModelForm, CommonControl):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(GroupForm, self).__init__(*args, **kwargs)

        # After creating the group, members can be controlled for a
        # dedicated page.
        if self.instance.pk:
            del self.fields['members']

        self.user_city = accounts.utils.get_user_city(self.user)
        self.user_gender = accounts.utils.get_user_gender(self.user)
    
        if not self.user.is_superuser and \
           not utils.is_bulb_coordinator_or_deputy(self.user):
            self.control_gender()

            
            if self.user_city == 'R':
                self.fields['city'].initial = 'R'
                self.fields['city'].choices = (
                    ('-', u'الرياض وجدة والأحساء'),
                    ('R', u'الرياض فقط'),
                )
            elif self.user_city == 'J':
                self.fields['city'].initial = 'A'
                self.fields['city'].choices = (
                    ('-', u'الرياض وجدة والأحساء'),
                    ('A', u'الأحساء فقط'),
                )
            elif self.user_city == 'J':
                self.fields['city'].initial = 'J'
                self.fields['city'].choices = (
                    ('-', u'الرياض وجدة والأحساء'),
                    ('J', u'جدة فقط'),
                )
    gender = forms.ChoiceField(choices=gender_choices, label=u"المجموعة تقبل عضوية")
    city = forms.ChoiceField(choices=city_choices, label=u"تشمل المجموعة")

    members = forms.ModelMultipleChoiceField(
                    widget=autocomplete.ModelSelect2Multiple(url='bulb:bulb-user-autocomplete',
                                                             attrs={
                                                                 'class': 'modern-style',
                                                                 'data-placeholder': 'أَضف طالبا',
                                                                 'data-minimum-input-length': 3
                                                             }),
                    label=u"الأعضاء",
                    queryset=User.objects.all(),
                    required=False)

    def save(self):
        group = super(GroupForm, self).save(commit=False)

        if self.user_gender == self.cleaned_data['gender']:
            group.is_limited_by_gender = True

        if self.user_city == self.cleaned_data['city']:
            group.is_limited_by_city = True

        group.save()
        return group

    class Meta:
        model = Group
        fields = ['name', 'image', 'description', 'category',
                  'is_private']

class FreeSessionForm(forms.ModelForm, CommonControl):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(FreeSessionForm, self).__init__(*args, **kwargs)

        self.user_city = accounts.utils.get_user_city(self.user)
        self.user_gender = accounts.utils.get_user_gender(self.user)

        # Limit the choice only if the user is not a superuser not a
        # Bulb coordinator.
        if not self.user.is_superuser and \
           not utils.is_bulb_coordinator_or_deputy(self.user):
            self.control_gender()

    def save(self):
        session = super(FreeSessionForm, self).save(commit=False)

        if self.user_gender == self.cleaned_data['gender']:
            session.is_limited_by_gender = True

        session.save()
        return session

    gender = forms.ChoiceField(choices=gender_choices, label=u"الجلسة تقبل حضور")

    class Meta:
        model = Session
        fields = ['title', 'agenda', 'location', 'date', 'start_time',
                  'end_time']

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'agenda', 'location', 'date', 'start_time',
                  'end_time']

class ReportForm(forms.ModelForm):
    attendees = forms.ModelMultipleChoiceField(
        widget=autocomplete.ModelSelect2Multiple(url='bulb:bulb-user-autocomplete',
                                                 attrs={
                                                     'class': 'modern-style',
                                                     'data-placeholder': 'أَضف طالبا',
                                                     'data-minimum-input-length': 3
                                                 }),
        label=u"الحضور",
        queryset=User.objects.all(),
        required=False)

    class Meta:
        model = Report
        fields = ['attendees']#, 'description']

class ReaderProfileForm(forms.ModelForm):

    def clean_twitter(self):
        data = self.cleaned_data['twitter']

        if not data:
            return data

        data = re.sub(u'^(?:https?://(?:m\.)?twitter\.com/)?@?', '', data)
        if not re.match(u'^[A-Za-z\d_]+$', data):
            raise  forms.ValidationError(u"أدخل اسم مستخدم صحيح.")
        else:
            return data

    def clean_goodreads(self):
        data = self.cleaned_data['goodreads']

        if not data:
            return data

        if not re.match(u'^(?:https?://)?(?:www.)?goodreads\.com/user/show/', data):
            raise  forms.ValidationError(u"أدخل رابط صفحتك على Goodreads.")
        else:
            # Because!
            data = re.sub('^http://', 'https://', data)
            if not re.match('^https?://', data):
                data = u"https://" + data
            return data

    class Meta:
        model = ReaderProfile
        fields = ['areas_of_interests', 'favorite_books',
                  'favorite_writers', 'average_reading',
                  'goodreads', 'twitter']

class RecruitmentForm(forms.ModelForm):
    class Meta:
        model = Recruitment
        exclude = ['user']
