# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django import forms
from . import models
from dal import autocomplete

class NominationForm(forms.ModelForm):
    class Meta:
        model = models.Nomination
        fields = ['city','position', 'plan', 'cv', 'certificates', 'gpa']

