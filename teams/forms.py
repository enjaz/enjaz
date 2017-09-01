# -*- coding: utf-8 -*-
from django import forms
from dal import autocomplete

from .models import Team, Position


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['ar_name','en_name','code_name','description', 'email',
                  'parent', 'leader', 'city', 'gender',
                  'category', 'logo', 'is_visible']
    def clean(self):
        # Remove spaces at the start and end of all text fields.
        cleaned_data = super(TeamForm, self).clean()
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()
        return cleaned_data


class DisabledTeamForm(TeamForm):
    def __init__(self, *args, **kwargs):
        # Fields to keep enabled.
        self.enabled_fields = ['description']
        # If an instance is passed, then store it in the instance variable.
        # This will be used to disable the fields.
        self.instance = kwargs.get('instance', None)

        # Initialize the form
        super(DisabledTeamForm, self).__init__(*args, **kwargs)

        # Make sure that an instance is passed (i.e. the form is being
        # edited).
        if self.instance:
            for field in self.fields:
                if not field in self.enabled_fields:
                    self.fields[field].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        cleaned_data = super(DisabledTeamForm, self).clean()
        if self.instance:
            for field in cleaned_data:
                if not field in self.enabled_fields:
                    cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data

class AddTeamMembersForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['members']

class EmailForm(forms.Form):
    subject = forms.CharField(label=u"العنوان")
    text = forms.CharField(label=u"اكتب نص رسالتك هنا", widget=forms.Textarea)

class AddPositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['position']