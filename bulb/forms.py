# -*- coding: utf-8  -*-
from django import forms
import autocomplete_light

from accounts.utils import get_user_gender
from bulb.models import Book, Group, Session, Report, Membership, ReaderProfile
from bulb import utils

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'edition',
                  'condition', 'description', 'cover',
                  'category']

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
                    ('', u'الطلاب والطالبات'),
                    ('F', u'الطالبات'),
                    )
            elif user_gender == 'M':
                initial_choice = 'M'
                gender_choices = (
                    ('', u'الطلاب والطالبات'),
                    ('M', u'الطلاب'),
                    )
            else: # Just in case
                initial_choice = ''
                gender_choices = (
                    ('', u'الطلاب والطالبات'),
                    ('F', u'الطالبات'),
                    ('M', u'الطلاب'),
                    )

            self.fields['gender'].choices = gender_choices
            self.fields['gender'].initial = initial_choice

    members = autocomplete_light.ModelMultipleChoiceField('BulbUserAutocomplete', label=u"الأعضاء", required=False)

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
    attendees = autocomplete_light.ModelMultipleChoiceField('BulbUserAutocomplete', label=u"الحضور", required=False)
    class Meta:
        model = Report
        fields = ['attendees', 'description']

class ReaderProfileForm(forms.ModelForm):
    class Meta:
        model = ReaderProfile
        fields = ['favorite_books', 'favorite_writers',
                  'areas_of_interests', 'average_reading',
                  'goodreads', 'twitter']
