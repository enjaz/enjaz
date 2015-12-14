# -*- coding: utf-8  -*-
from django import forms

from hpc.models import Abstract

class AbstractForm(forms.ModelForm):
    class Meta:
        model = Abstract
        fields = ['title', 'authors', 'university', 'college',
                  'presenting_author', 'email', 'phone', 'level',
                  'presentation_preference', 'attachment']
