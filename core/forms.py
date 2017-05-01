# -*- coding: utf-8  -*-
from django import forms

from constance import config

# This form is used in the admin interface to make all fields
# optional.  Check out events/admin.py.
class OptionalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OptionalForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False

class DebateForm(forms.Form):
    url = forms.URLField(required=False)

    def save(self):
        config.DEBATE_URL = self.cleaned_data['url']
