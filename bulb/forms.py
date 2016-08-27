# -*- coding: utf-8  -*-
import re

from django.contrib.auth.models import User
from django import forms
from dal import autocomplete

from accounts.utils import get_user_gender
from bulb.models import Book, Request, Group, Session, Report, Membership, ReaderProfile
from bulb import utils

class BookEditForm(forms.ModelForm):
    """Form used to edit books. It allows changing contribution type from
       giving to lending."""
    class Meta:
        model = Book
        fields = ['title', 'authors', 'edition', 'pages',
                  'condition', 'description', 'cover',
                  'category', 'contribution',
                  'available_until']

class BookGiveForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'edition', 'pages',
                  'condition', 'description', 'cover',
                  'category']

class BookLendForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'edition', 'pages', 'condition',
                  'description', 'cover', 'category',
                  'available_until']

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

        requester_gender = get_user_gender(self.instance.requester)
        owner_gender = get_user_gender(self.instance.book.submitter)
        if data == 'I' or  requester_gender != owner_gender:
            delivery = 'I'
        else:
            delivery = 'D'

        return delivery

    class Meta:
        model = Request
        fields = ['delivery', 'borrowing_end_date']
        widgets  = {'delivery': forms.HiddenInput()}

class GroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(GroupForm, self).__init__(*args, **kwargs)

        # After creating the group, members can be controlled for a
        # dedicated page.
        if self.instance.pk:
            del self.fields['members']

        # Limit the choice only if the user is not a superuser not a
        # Bulb coordinator.
        if not user.is_superuser and \
           not utils.is_bulb_coordinator_or_deputy(user):
            user_gender = get_user_gender(user)
            if user_gender == 'F':
                initial_choice = 'F'
                gender_choices = (
                    #('', u'الطلاب والطالبات'),
                    ('F', u'الطالبات'),
                    )
            elif user_gender == 'M':
                initial_choice = 'M'
                gender_choices = (
                    #('', u'الطلاب والطالبات'),
                    ('M', u'الطلاب'),
                    )
            else: # Just in case
                #initial_choice = ''
                initial_choice = 'M'
                gender_choices = (
                    #('', u'الطلاب والطالبات'),
                    ('F', u'الطالبات'),
                    ('M', u'الطلاب'),
                    )

            self.fields['gender'].choices = gender_choices
            self.fields['gender'].initial = initial_choice

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

    class Meta:
        model = Group
        fields = ['name', 'image', 'description', 'gender',
                  'category']

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
        fields = ['attendees', 'description']

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
