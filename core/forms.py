# -*- coding: utf-8  -*-
from django import forms

from constance import config

class DebateForm(forms.Form):
    url = forms.URLField(required=False)

    def save(self):
        config.DEBATE_URL = self.cleaned_data['url']
